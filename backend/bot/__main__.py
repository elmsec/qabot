import os
import sys
import logging
import traceback
import gettext

from time import sleep
from secrets import token_hex
from html import escape as html_escape
from functools import wraps
from peewee import IntegrityError

from telegram import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InlineQueryResultArticle,
    InputTextMessageContent,
)
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    InlineQueryHandler,
    Filters,
    PicklePersistence,
)
from telegram.error import (
    Unauthorized
)
from telegram.utils.helpers import (
    create_deep_linked_url,
    mention_html as mh
)

from data.db import User, Question, Settings

# Enable logging
log_format = (
    '%(asctime)s - [%(filename)s:%(lineno)s] - %(levelname)s - %(message)s')
logging.basicConfig(
    format=log_format,
    level=logging.INFO)
logger = logging.getLogger(__name__)

# Logging: File Handler
fh = logging.FileHandler('all.log')
fh.setLevel(logging.INFO)
fh.setFormatter(logging.Formatter(log_format))
logger.addHandler(fh)


# CONSTANTS
WEB_APP_NAME = os.getenv('WEB_APP_NAME')
ADMIN_IDs = os.getenv('ADMIN_IDs').split(',')
ALLOWED_CHATS = os.getenv('ALLOWED_CHATS').split(',')

IS_DEV = os.getenv('DEVELOPMENT', None)

LIST_OF_ADMINS = [int(i) for i in ADMIN_IDs]
LIST_OF_ALLOWED_CHATS = [int(i) for i in ALLOWED_CHATS]

TYPING_QUESTION, CHECKING_QUESTION = range(2)
TYPING_ANSWER, CHECKING_ANSWER = range(2)


# TRANSLATIONS
en = gettext.translation(
    'exampleQAbot', 'locale', languages=['en'], fallback=True)
tr = gettext.translation(
    'exampleQAbot', 'locale', languages=['tr'], fallback=True)
LANGUAGES = {
    'en': en,
    'tr': tr,
}
_ = LANGUAGES['en'].gettext


QUESTION_STATUS_LIST = [
    _("sent"), _("delivered"), _("answered"), _("not delivered")]


def mention_html(user, telegram_name=None, telegram=False):
    if telegram:
        return mh(user, telegram_name)

    settings = user.settings.get()
    anon_name = f"User ({user.link})"
    name = user.get_full_name()
    result = anon_name if settings.hide_name else name

    if not settings.hide_profile and not settings.hide_name:
        result = mh(user.telegram_id, result)

    return result


def set_language(lang):
    global _
    _ = LANGUAGES.get(lang, LANGUAGES["en"]).gettext


def user_restricted(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        start(update, context, silent=True)
        return func(update, context, *args, **kwargs)
    return wrapped


def translate(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user_lang = update.effective_user.language_code or 'en'
        set_language(user_lang)
        return func(update, context, *args, **kwargs)
    return wrapped


def restricted(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in LIST_OF_ADMINS:
            logger.critical(
                "Unauthorized access denied for {}.".format(user_id))
            return
        return func(update, context, *args, **kwargs)
    return wrapped


def start_message(user_id):
    user = User.get_or_none(User.telegram_id == user_id)

    if not user:
        return logger.error('user not found', exc_info=1)

    message = _(
        "👋 Hello, <b>{user}</b>!\n\n"
        "I can help you get anonymous questions and messages "
        "from people. \n\n"

        "Share your link with people and wait for someone "
        "to ask or say something interesting to you. If you answer the "
        "message of that person, I will deliver your answer as well! "
    ).format(user=html_escape(user.get_full_name()))
    keyboard = [
        InlineKeyboardButton(
            _("📥 Inbox"), callback_data="inbox:{}:1".format(user.link)),
        InlineKeyboardButton(
            _("📤 Outbox"), callback_data="outbox:{}:1".format(user.link)),
        InlineKeyboardButton(
            _("🔗 My Link"), callback_data="load:link"),
        InlineKeyboardButton(
            _("⚙️ Settings"), callback_data="load:settings"),
        InlineKeyboardButton(
            _("📢 Channel"), url="https://t.me/{}".format(
                os.getenv("CHANNEL_USERNAME")
            ),
        ),
    ]
    reply_markup = InlineKeyboardMarkup(build_menu(keyboard, 2))
    return (message, reply_markup)


@translate
def start(update, context, silent=False, reference=None):
    u = update.effective_user
    created = None
    try:
        user, created = User.get_or_create(
            telegram_id=u.id,
            defaults=dict(
                username=u.username,
                first_name=u.first_name,
                last_name=u.last_name if u.last_name else None,
                language=getattr(u, 'language_code', 'en'),
                reference=reference,
            )
        )
        if created:
            Settings.create(user=user)
    except Exception as e:
        message = _("An error occurred. Please come back later.")
        context.bot.send_message(u.id, message, "HTML")
        return logger.error(e)
    finally:
        if silent and not created:
            return

        message, reply_markup = start_message(u.id)
        context.bot.send_message(
            u.id, message, "HTML", reply_markup=reply_markup)


def build_msg_with_btns(message, buttons, cols=1):
    keyboard = build_inline_buttons(buttons)
    reply_markup = InlineKeyboardMarkup(build_menu(keyboard, cols))
    return (message, reply_markup)


def build_user_profile(context_user, context):
    questions = context_user.inbox
    questions_count = questions.count()
    answered_questions = questions.where(
        Question.answer.is_null(False)).count()
    answered_percentage = round(answered_questions/questions_count*100, 2)\
        if questions_count > 0 else 0

    message = _(
        "<b>User:</b> {user}\n"
        "<b>Questions:</b> {questions}\n"
        "<b>Answered:</b> {answered} (%{answered_percentage})\n\n"
        "Ask <b>{user}</b> an <b>anonymous</b> question or see the recent "
        "questions asked before."
    ).format(
        user=mention_html(context_user),
        questions=questions_count,
        answered=answered_questions,
        answered_percentage=answered_percentage,
    )

    keyboard = [
        [
            _("🚀 Open in mini app [NEW!]"),
            "",
            (
                f"https://t.me/{context.bot.get_me().username}/"
                f"{WEB_APP_NAME}?startapp={context_user.link}"
            ),
        ],
        [_("📨 Ask a question"), "ask_question:%s" % context_user.link],
        [_("📥 Show asked questions"), "inbox:%s:1" % context_user.link],
    ]

    return build_msg_with_btns(message, keyboard)


@translate
def start_args(update, context):
    """
    /start command with an arg like zn3ja19sh1
    """
    if not context.args or len(context.args[0]) != 10:
        return

    context_user = User.get_or_none(User.link == context.args[0])
    start(update, context, silent=True, reference=context_user)

    if not context_user:
        message = _("Sorry, the link you used is invalid.")
        return update.message.reply_html(message)

    message, reply_markup = build_user_profile(context_user, context=context)
    update.message.reply_html(message, reply_markup=reply_markup)


def build_settings(user):
    message = _(
        "<b>Hide my name:</b> If on, people will not see your name when they "
        "are asking you a question or vieweing questions asked to you.\n\n"
        "<b>Hide my profile:</b> If on, people will not be able to go to "
        "your Telegram profile by clicking on your name (only works when "
        "the \"Hide my name\" option is off).\n\n"
        "<b>Notify for questions:</b> If on, you get a notification "
        "when a user asked you a question.\n\n"
        "<b>Notify for answers:</b> If on, you get a notification "
        "when a user answered your question.\n\n"
    )

    s = Settings.get(Settings.user == user)
    emojis = ["➖", "✅"]
    buttons = build_inline_buttons([
        [_("Hide my name"), "empty"],
        [emojis[s.hide_name], "settings:hide_name"],

        [_("Hide my profile"), "empty"],
        [emojis[s.hide_profile], "settings:hide_profile"],

        [_("Notify for questions"), "empty"],
        [emojis[s.question_notification], "settings:question_notification"],

        [_("Notify for answers"), "empty"],
        [emojis[s.answer_notification], "settings:answer_notification"],
    ])
    footer = build_back_button("start")
    keyboard = build_menu(buttons, 2, footer_buttons=footer)
    reply_markup = InlineKeyboardMarkup(keyboard)

    return (message, reply_markup)


@translate
def settings(update, context):
    allowed_attrs = [
        "hide_name",
        "hide_profile",
        "question_notification",
        "answer_notification"]
    cq = update.callback_query
    data = cq.data.split(':')[1]

    if data not in allowed_attrs:
        return cq.answer(_("Invalid or unallowed."))

    attr = getattr(Settings, data)
    user = User.get(User.telegram_id == update.effective_user.id)
    new_value = 1 if getattr(user.settings.get(), data) == 0 else 0
    query = Settings.update({attr: new_value}).where(Settings.user == user)
    query.execute()
    message, reply_markup = build_settings(user)

    cq.message.edit_text(message, parse_mode="HTML", reply_markup=reply_markup)
    cq.answer()


@translate
def settings_command(update, context):
    user = User.get(User.telegram_id == update.effective_user.id)
    message, reply_markup = build_settings(user)
    update.message.reply_html(message, reply_markup=reply_markup)


@translate
def callback_loader(update, context):
    cq = update.callback_query
    reply_markup = None

    if 'load:link' == cq.data:
        user = User.get(User.telegram_id == update.effective_user.id)
        user_deep_link = create_deep_linked_url(
            context.bot.get_me().username, user.link)

        message = _(
            "🤩 You are in the right place to learn how to get new questions "
            "from people! There are two methods to do this. \n\n"
            "<b>1. Share a message with a button</b> <i>(recommended)</i>\n"
            "The best solution if your target audience is on Telegram. "
            "Just use the <i>Share as a message</i> button below and choose "
            "a chat to post. It generates a message with a button that "
            "allows users to ask you a new question and see the questions "
            "asked to you. Alternatively, you can type a custom message "
            "after choosing a chat.\n\n"
            "<b>2. Share your link</b>\n"
            "You can copy this <a href='{user_deep_link}'>link</a> and "
            "paste it wherever people see it. "
            "When a user clicks on this link, it will start a conversation "
            "with me on Telegram and the user will be able to ask you a "
            "new question, or see the questions asked to you.\n\n"
            "<b>Note:</b>\n"
            "You can hide your Telegram name and profile from people who "
            "ask you questions. Check the /settings menu. \n\n"
            "That's all!"
            ).format(user_deep_link=user_deep_link)

        keyboard = [
            InlineKeyboardButton(
                _("Share as a message"), switch_inline_query=""),
            build_back_button("start")]
        reply_markup = InlineKeyboardMarkup(build_menu(keyboard, 1))
    elif 'load:profile:' in cq.data:
        context_user = User.get(User.link == cq.data.split(':')[2])
        message, reply_markup = build_user_profile(
            context_user, context=context)
    elif 'load:start' == cq.data:
        message, reply_markup = start_message(update.effective_user.id)
    elif 'load:settings' == cq.data:
        user = User.get(User.telegram_id == update.effective_user.id)
        message, reply_markup = build_settings(user)

    cq.message.edit_text(
        message,
        disable_web_page_preview=True,
        reply_markup=reply_markup,
        parse_mode='HTML')
    cq.answer()


@translate
def ask_question(update, context):
    cq = update.callback_query
    data = cq.data.split(':')[1]

    user = User.get(User.link == data)

    # TODO: enable in production?
    # if user.telegram_id == update.effective_user.id:
    #     cq.answer(_("❗️ You can not ask yourself a question."))
    #     return ConversationHandler.END

    update.effective_user.send_message(_(
        "Please type your anonymous question. "
        "You'll be able to check it before sending."))

    context.user_data["question"] = {}
    context.user_data["question"]["context_user"] = user
    cq.answer()

    return TYPING_QUESTION


@translate
def question_typed(update, context):
    count = len(update.message.text)
    if count > 200:
        update.message.reply_text(_(
            "A question can be a maximum of 200 characters, but "
            "your question is {count} characters long."
        ).format(count=count))
        return TYPING_QUESTION

    user_data = context.user_data
    context_user = user_data["question"]["context_user"]
    keyboard = [
        [
            InlineKeyboardButton("✅ Send", callback_data="send"),
            InlineKeyboardButton("📝 Edit", callback_data="edit")
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    user_data["question"]["text"] = html_escape(update.message.text)
    message = _(
        "<b>Your anonymous question:</b>\n"
        "<i>{}</i>\n\n"
        "If you are okay with this, I will send the question to "
        "<b>{}</b> anonymously. Your identity will be kept hidden.\n\n"
        "To cancel it, use /cancel."
    )
    message = message.format(
        user_data["question"]["text"], mention_html(context_user))
    sent = update.message.reply_html(message, reply_markup=reply_markup)

    user_data["question"]["last_message"] = sent

    return CHECKING_QUESTION


@translate
def question_checked(update, context):
    u = update.effective_user
    cq = update.callback_query
    data = cq.data

    cq.answer()
    if data == 'edit':
        cq.message.edit_text(_(
            "Please type your anonymous question. You'll be able to check it "
            "before sending."),
            parse_mode="HTML")
        return TYPING_QUESTION
    elif data == 'send':
        cq.message.edit_text(_("Please wait. Sending..."))
        sleep(1)

        user = User.get(User.telegram_id == u.id)
        user_data = context.user_data

        try:
            new_question = Question(
                sender=user,
                to=user_data["question"]["context_user"],
                text=user_data["question"]["text"])
            new_question.save()
        except IntegrityError:
            new_question.link = token_hex(5)
            new_question.save()
        except Exception as e:
            message = _("Sorry, an error occurred.")
            logger.error(e)
        else:
            message = _(
                "✅ Your question has been <b>successfully</b> sent! "
                "You can see the status of your question with /view_{}"
            ).format(new_question.link)
        finally:
            del user_data["question"]
            cq.message.edit_text(message, parse_mode="HTML")
            return ConversationHandler.END


@translate
def answer_question(update, context):
    cq = update.callback_query
    question_link = cq.data.split(':')[1]
    question = Question.get(Question.link == question_link)

    context.user_data["answer"] = {}
    context.user_data["answer"]["question"] = question

    message = _(
        "<b>Question:</b>\n<i>{question}</i>\n\n"
        "Please type your answer for this question. You'll be able to check "
        "it before sending. ").format(question=html_escape(question.text))
    cq.message.edit_text(message, parse_mode="HTML")

    if context.user_data.get("question_message"):
        del context.user_data["question_message"]

    cq.answer()
    return TYPING_ANSWER


@translate
def answer_typed(update, context):
    count = len(update.message.text)
    if count > 200:
        update.message.reply_text(_(
            "An answer can be a maximum of 200 characters, but "
            "your answer is {count} characters long."
        ).format(count=count))
        return TYPING_ANSWER

    user_data = context.user_data
    keyboard = [[
        InlineKeyboardButton(_("✅ Publish"), callback_data="send"),
        InlineKeyboardButton(_("📝 Edit"), callback_data="edit")
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    user_data["answer"]["text"] = update.message.text
    message = _(
        "<b>Your answer:</b>\n"
        "<i>{}</i>\n\n"
        "If you are okay with this, I will publish it and send that "
        "answer to the person who asked the question. \n\n"
        "To cancel it, use /cancel."
    ).format(html_escape(user_data["answer"]["text"]))
    sent = update.message.reply_html(message, reply_markup=reply_markup)

    user_data["answer"]["last_message"] = sent

    return CHECKING_ANSWER


@translate
def answer_checked(update, context):
    cq = update.callback_query
    data = cq.data
    user_data = context.user_data
    question = user_data["answer"]["question"]

    cq.answer()
    if data == 'edit':
        cq.message.edit_text(_(
            "<b>Question:</b>\n<i>{question}</i>\n\n"
            "Please type your answer for this question. You'll be able to "
            "check it before sending.").format(
                question=html_escape(question.text)),
            parse_mode="HTML")
        return TYPING_ANSWER
    elif data == 'send':
        cq.message.edit_text(_("Please wait. Publishing..."))

        try:
            question.answer = user_data["answer"]["text"]
            question.save()
        except Exception as e:
            message = _("Sorry, an error occurred.")
            logger.error(e)
        else:
            message = _(
                "✅ Your answer has been <b>successfully</b> published!")
        finally:
            del user_data["answer"]
            cq.message.edit_text(message, parse_mode="HTML")
            return ConversationHandler.END


@translate
def cancel(update, context):
    user_data = context.user_data

    if user_data.get("question", {}).get("last_message"):
        user_data["question"]["last_message"].edit_reply_markup()
        del user_data["question"]

    if user_data.get("answer", {}).get("last_message"):
        user_data["answer"]["last_message"].edit_reply_markup()
        del user_data["answer"]

    update.message.reply_text(_("The operation was cancelled."))
    return ConversationHandler.END


def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu


def build_inline_buttons(buttons):
    button_list = []
    for button in buttons:
        url = None
        # workaround
        if len(button) == 2:
            text, callback = button
        elif len(button) == 3:
            text, callback, url = button
        b = InlineKeyboardButton(text, callback_data=callback, url=url)
        button_list.append(b)
    return button_list


def build_pages(total, cb_prefix="", selected=None):
    new_buttons = []
    for no in range(1, total+1):
        btn_text = no
        callback = cb_prefix + str(no)
        if no == selected:
            btn_text = "· {} ·".format(no)
            callback = 'empty'
        new_buttons.append(
            InlineKeyboardButton(btn_text, callback_data=callback))
    return new_buttons


def build_questions_list(questions, owner=None, own=False, outbox=False):
    message = _(
        "📥 <b>Question List</b>\n"
        "Here you can find a list of the questions asked to <b>{user}</b>.\n\n"
        ).format(user=mention_html(owner))
    if outbox:
        message = _(
            "📤 <b>Questions you asked</b>\n"
            "Here you can find a list of the questions you asked.\n\n")
    elif own:
        message = _(
            "📥 <b>Questions asked to you</b>\n"
            "Here you can find a list of the questions asked to you. You can "
            "answer or delete a question by using its menu command. "
            "That's all!\n\n")

    for q in questions:
        to = ""
        if outbox:
            to = "👤 {to} · ".format(
                to=mention_html(q.to))
        message += _(
            "💭 <b>Question:</b>\n {question}\n\n"
            "🗯 <b>Answer:</b>\n {answer}\n\n"
            "{to}🎯 <i>{status}</i> · /view_{question_link}\n\n"
            "➖➖➖➖➖➖➖➖➖➖➖➖"
            "\n\n"
        ).format(
            question=html_escape(q.text),
            question_link=q.link,
            answer=html_escape(q.answer) if q.answer else "—",
            to=to,
            status=_(QUESTION_STATUS_LIST[q.status]))
    return message


def build_back_button(callback):
    callback = "load:" + callback
    return InlineKeyboardButton(_("« Back"), callback_data=callback)


@translate
def inbox_outbox(update, context):
    """
    Inbox to show asked questions of a user
    """
    print("HEY")
    u = update.effective_user
    cq = update.callback_query
    user_link = cq.data.split(':')[1]
    page = int(cq.data.split(':')[2])
    user = User.get(User.link == user_link)
    box, term = (user.inbox, 'inbox') if 'inbox' in cq.data\
        else (user.outbox, 'outbox')
    own = user.telegram_id == u.id
    box_count = box.count()

    if box_count <= 0:
        return cq.answer(_("😞 No questions asked yet."))

    paginate_by = 2 if box_count < 30 else 4
    total_pages = round(box_count/paginate_by) or 1

    questions = box.paginate(page, paginate_by)
    questions = questions.order_by(Question.created.desc())
    keyboard = build_pages(total_pages, "{}:{}:".format(term, user_link), page)
    profile_cb = "start" if own else ("profile:%s" % user_link)
    reply_markup = InlineKeyboardMarkup(
        build_menu(keyboard, 4, footer_buttons=build_back_button(profile_cb)))

    cq.answer()
    message = build_questions_list(questions, user, own, term == 'outbox')
    cq.message.edit_text(message, reply_markup=reply_markup, parse_mode="HTML")


@translate
def question_menu(update, context):
    u = update.effective_user
    user = User.get(User.telegram_id == u.id)
    user_data = context.user_data

    question_link = update.message.text.split('/view_')[1]
    question = Question.get_or_none(Question.link == question_link)

    if not question:
        return update.message.reply_text(_("There's no such question."))

    message = _(
        "<b>Question Menu</b>\n"
        "Here you can see the details of this question.\n\n"
        "💭 <b>Question:</b>\n {question}\n\n"
        "🗯 <b>Answer:</b>\n {answer}\n\n"
        "👤 {to} · 🎯 <i>{status}</i>\n\n"
    ).format(
        to=mention_html(question.to),
        question=html_escape(question.text),
        answer=html_escape(question.answer) if question.answer else "—",
        status=_(QUESTION_STATUS_LIST[question.status])
    )

    reply_markup = None
    if question.to == user:
        # that's the user's own question
        message += _(
            "You can delete or answer this question with the "
            "buttons below.")
        answer_btn = _("📝 Edit Answer") if question.answer else _("📝 Answer")
        buttons = build_inline_buttons([
            [answer_btn, "answer:%s" % question.link],
            [_("❌ Delete"), "delete_question:%s" % question.link]])
        reply_markup = InlineKeyboardMarkup(build_menu(buttons, 2))

    question_message = user_data.get("question_message")
    if question_message and question_message.reply_markup:
        try:
            question_message.edit_reply_markup()
        except Exception:
            # user deleted the saved message
            pass

    sent = update.message.reply_html(message, reply_markup=reply_markup)
    user_data["question_message"] = sent


@translate
def delete_question(update, context):
    cq = update.callback_query
    data = cq.data
    datas = data.split(':')
    question = Question.get(Question.link == datas[1])
    user_data = context.user_data

    keyboard = None
    if ':yes' in data:
        question.delete_instance()
        cq.message.edit_text(
            _("The question was <b>successfully</b> deleted."),
            parse_mode="HTML", reply_markup=None)
        del user_data["question_message"]
        return cq.answer()
    elif ':no' in data:
        # cancel
        answer_btn = _("📝 Edit Answer") if question.answer else _("📝 Answer")
        keyboard = build_inline_buttons([
            [answer_btn, "answer:%s" % question.link],
            [_("❌ Delete"), "delete_question:%s" % question.link]])
    else:
        # show alert
        keyboard = build_inline_buttons([
            [
                _("😏 Yes, delete"),
                "delete_question:{}:yes".format(question.link)],
            [
                _("🤨 No, cancel"),
                "delete_question:{}:no".format(question.link)]
        ])

    if keyboard:
        reply_markup = InlineKeyboardMarkup(build_menu(keyboard, 2))
        cq.message.edit_reply_markup(reply_markup=reply_markup)


def messenger(context):
    waiting_questions = (Question.select().where(
        (Question.status == 0) |
        ((Question.status == 1) & (Question.answer.is_null(False)))))
    q_message = (
        "🤓 Hey, someone has asked you a new question! To view the "
        "question, use this command: /view_{question_link}")
    a_message = (
        "🤓 Hey, {user} has answered your question! To view the "
        "answer, use this command: /view_{question_link}")

    for question in waiting_questions[:15]:
        message = None
        if question.status == 0:
            to = question.to
            settings = to.settings.get()

            if settings.question_notification:
                message = q_message.format(question_link=question.link)
        elif question.status == 1:
            to = question.sender
            settings = to.settings.get()
            user_mention = mention_html(question.to)

            if settings.answer_notification:
                message = a_message.format(
                    user=user_mention,
                    question_link=question.link)

        try:
            if message and to.bot_permission:
                set_language(to.language)
                context.bot.send_message(
                    to.telegram_id, _(message), parse_mode="HTML")
        except Unauthorized:
            to.bot_permission = False
            to.save()
            question.status = 3
        else:
            question.status = question.status + 1

        question.save()
        sleep(1)


@translate
def error(update, context):
    """Log Errors caused by Updates."""

    # add all the dev user_ids in this list. You can also add ids of channels
    #  or groups.
    devs = LIST_OF_ALLOWED_CHATS

    # This will always work, but will
    # not notify users if the update is a callback or am inline query, or a
    # poll update. In case you want this, keep in mind that sending the
    # message could fail
    if update.effective_message:
        message = _(
            "Sorry, an error happened while processing your request. "
            "We will check the problem and fix it accordingly.\n\n"
            "You can try again, come back later or use /start."
        )
        update.effective_message.reply_text(message)

    trace = "".join(traceback.format_tb(sys.exc_info()[2]))

    # lets try to get as much information from the telegram update as possible
    payload = ""

    # normally, we always have an user. If not, its either a channel or a
    # poll update
    if update.effective_user:
        u = update.effective_user
        payload += f' with the user {mention_html(u.id, u.first_name, True)}'

    # there are more situations when you don't get a chat
    if update.effective_chat:
        payload += f' within the chat <i>{update.effective_chat.title}</i>'
        if update.effective_chat.username:
            payload += f' (@{update.effective_chat.username})'

    if update.poll:
        payload += f' with the poll id {update.poll.id}.'

    text = (
        f"Hey. There's a problem with @{context.bot.get_me().username}.\n"
        f"The error <code>{context.error}</code> happened{payload}. "
        f"The full traceback:\n\n<code>{trace}</code>")

    logger.warning(
        '\n\nUpdate: \n"%s"\n\nCaused error: \n"%s"\n\nWith: %s',
        update, trace, context.error)

    if "Message is not modified" in context.error:
        return

    if not IS_DEV:
        for dev_id in devs:
            context.bot.send_message(dev_id, text, parse_mode="HTML")


@translate
def unallowed_join(update, context):
    if update.effective_chat.id in LIST_OF_ALLOWED_CHATS:
        return

    message = (
        "👋 Hey, please do not add me to other chats. "
    )
    try:
        update.effective_chat.send_message(message)
    finally:
        update.effective_chat.leave()
        raise Exception


@restricted
@translate
def test(update, context):
    # global _
    # _ = tr.gettext
    message = mention_html(update.effective_user.id, "You!", True)
    update.message.reply_html(update.message.text_html)
    update.message.reply_html(message)
    raise Exception("ERROR.....")


@restricted
def stats(update, context):
    users = User.select().count()
    questions = Question.select().count()
    answered = Question.select().where(Question.answer.is_null(False)).count()

    message = _(
        "📊 <b>STATS</b>\n"
        "<b>Registered Users:</b> {users}\n"
        "<b>Asked Questions:</b> {questions}\n"
        "<b>Answered Questions:</b> {answered}\n\n"
    ).format(
        users=users,
        questions=questions,
        answered=answered,
    )
    update.message.reply_html(message)


def empty_callback(update, context):
    cq = update.callback_query
    cq.answer()


@translate
@user_restricted
def inline_query(update, context):
    query = update.inline_query.query

    user = User.get_or_none(
        User.telegram_id == update.effective_user.id)

    if not user:
        return

    deep_link = create_deep_linked_url(
        context.bot.get_me().username, user.link)

    questions = user.inbox
    questions_count = questions.count()
    answered_questions = questions.where(
        Question.answer.is_null(False)).count()
    answered_percentage = round(
        answered_questions/questions_count*100, 2)\
        if questions_count > 0 else 0

    description = _(
        "<b>User:</b> {user}\n"
        "<b>Questions:</b> {questions}\n"
        "<b>Answered:</b> {answered} (%{answered_percentage})\n\n"
    ).format(
        user=mention_html(user),
        questions=questions_count,
        answered=answered_questions,
        answered_percentage=answered_percentage,
    )

    default_message = _(
        "👻 Hey! Using the button below 👇, you can ask me an "
        "anonymous question or see the recent questions asked to me.")

    message = query or default_message
    description += message

    reply_markup = InlineKeyboardMarkup.from_button(
        InlineKeyboardButton(_("👉 Start"), deep_link))

    results = [
        InlineQueryResultArticle(
            id=token_hex(10),
            title=_("👉 Touch here to share!"),
            description=message,
            input_message_content=InputTextMessageContent(
                description, parse_mode="HTML"),
            reply_markup=reply_markup),
    ]
    update.inline_query.answer(results, cache_time=5, is_personal=True)


def main():
    """Run bot."""
    # persistence
    my_persistence = PicklePersistence(filename="persistence.file")

    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(
        os.getenv("BOT_TOKEN"),
        persistence=my_persistence,
        use_context=True)

    # Periodically save jobs
    job_queue = updater.job_queue
    job_queue.run_repeating(messenger, 30)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler(
        "start", start_args,
        pass_args=True,
        filters=Filters.regex(r"(\w{10})$")))
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(callback_loader, pattern=r"^load:"))
    dp.add_handler(CallbackQueryHandler(
        inbox_outbox, pattern=r"(^inbox:|^outbox:)"))
    dp.add_handler(CallbackQueryHandler(
        delete_question, pattern=r"^delete_question:"))

    dp.add_handler(CallbackQueryHandler(
        settings, pattern=r"^settings:"))

    dp.add_handler(CommandHandler("settings", settings_command))

    dp.add_handler(CallbackQueryHandler(empty_callback, pattern=r"^empty$"))
    dp.add_handler(MessageHandler(
        Filters.regex(r"^/view_([0-9a-zA-Z]{10})$"),
        question_menu,
        pass_user_data=True))
    dp.add_handler(MessageHandler(
        Filters.status_update.new_chat_members, unallowed_join))
    dp.add_handler(MessageHandler(~ Filters.private, unallowed_join))
    dp.add_handler(InlineQueryHandler(inline_query))
    dp.add_handler(CommandHandler("stats", stats))
    dp.add_handler(CommandHandler("test", test))

    question_conv_handler = ConversationHandler(
        name="question_conversation",
        persistent=True,
        allow_reentry=True,
        entry_points=[
            CallbackQueryHandler(
                ask_question,
                pattern=r"ask_question:(\w{10})",
                pass_user_data=True)],
        states={
            TYPING_QUESTION: [
                MessageHandler(
                    Filters.text, question_typed, pass_user_data=True),
            ],
            CHECKING_QUESTION: [
                CallbackQueryHandler(question_checked, pattern=r"(send|edit)")
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    dp.add_handler(question_conv_handler)

    answer_conv_handler = ConversationHandler(
        name="answer_conversation",
        persistent=True,
        allow_reentry=True,
        entry_points=[
            CallbackQueryHandler(
                answer_question,
                pattern=r"answer:(.+)",
                pass_user_data=True)],
        states={
            TYPING_ANSWER: [MessageHandler(
                Filters.text, answer_typed, pass_user_data=True),
            ],
            CHECKING_ANSWER: [
                CallbackQueryHandler(answer_checked, pattern=r"(send|edit)")
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(answer_conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()

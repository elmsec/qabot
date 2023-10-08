import os
import peewee
from datetime import datetime
from secrets import token_hex


# DB CONNECTION (SQLite)
# DB = peewee.SqliteDatabase('bot.db', pragmas={'foreign_keys': 1})
DB = peewee.PostgresqlDatabase(
    os.environ.get("SQL_DATABASE", "qabot"),
    user=os.environ.get("SQL_USER", "qabot"),
    password=os.environ.get("SQL_PASSWORD", "qabot"),
    host=os.environ.get("SQL_HOST", "localhost"),
    port=os.environ.get("SQL_PORT", "5432")
)


class BaseDatabaseModel(peewee.Model):
    """
        Base database model
    """
    class Meta:
        database = DB


class User(BaseDatabaseModel):
    """
        User model for the database.
        It contains all users who used the bot
    """
    telegram_id = peewee.IntegerField(unique=True)
    first_name = peewee.CharField(max_length=100)
    last_name = peewee.CharField(max_length=100, null=True)
    username = peewee.CharField(max_length=40, null=True)
    link = peewee.CharField(
        max_length=10, default=lambda: token_hex(5), unique=True)
    bot_permission = peewee.BooleanField(default=True)
    language = peewee.CharField(max_length=10, default='en')
    reference = peewee.ForeignKeyField('self', backref='references', null=True)
    created = peewee.DateTimeField(default=datetime.now)

    def get_full_name(self):
        return (self.first_name + ' ' + (self.last_name or '')).strip()


class Question(BaseDatabaseModel):
    """
    Question model for the asked questions
    """
    sender = peewee.ForeignKeyField(User, backref='outbox')
    to = peewee.ForeignKeyField(User, backref='inbox')
    text = peewee.CharField()
    answer = peewee.CharField(null=True)
    status = peewee.SmallIntegerField(default=0)
    link = peewee.CharField(
        max_length=10, default=lambda: token_hex(5), unique=True)
    created = peewee.DateTimeField(default=datetime.now)


class Settings(BaseDatabaseModel):
    """
    Settings model for users
    """
    user = peewee.ForeignKeyField(User, backref="settings")
    hide_name = peewee.SmallIntegerField(default=0)
    hide_profile = peewee.SmallIntegerField(default=0)
    question_notification = peewee.SmallIntegerField(default=1)
    answer_notification = peewee.SmallIntegerField(default=1)


def initialize_db(db):
    db.connect()
    db.create_tables([User, Question, Settings], safe=True)
    db.close()


initialize_db(DB)

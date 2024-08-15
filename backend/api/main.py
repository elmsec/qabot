import os
from typing import List
from datetime import timedelta

from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


from data.db import User, Question, Settings
from api.dtos import schemas
from api.utils.web_app_data_validator import WebAppDataHelper
from api.constants import auth_constants
from api.utils.auth import get_current_user, create_access_token


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  # TODO: production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    web_app_data: str | None = None


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: TokenData):
    validator = WebAppDataHelper(
        form_data.web_app_data,
        bot_token=os.getenv('BOT_TOKEN'),
        diff=auth_constants.WEBP_APP_DATA_DIFF)

    if not validator.is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect web app data",
            headers={"WWW-Authenticate": "Bearer"})

    telegram_id = validator.parsed_user_data['id']
    user = User.get_or_none(User.telegram_id == telegram_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(
        minutes=auth_constants.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.link}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/")
async def root():
    return {"message": "We love Telegram!"}


# users/me
@app.get("/users/me", response_model=schemas.User)
async def read_users_me(current_user: dict = Depends(get_current_user)):
    user = User.get_or_none(User.link == current_user['sub'])
    return user


@app.get("/questions/{question_link}", response_model=schemas.Question)
async def read_question(question_link: str):
    question = Question.get_or_none(Question.link == question_link)
    return question


@app.get("/users/{user_link}", response_model=schemas.User)
async def read_user(user_link: str):
    user = User.get_or_none(User.link == user_link)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    settings: Settings = user.settings.get()
    if settings.hide_name or settings.hide_profile:
        user.first_name = "Anonymous"
        user.username = None
        user.telegram_id = None

    return user


@app.get(
    "/users/me/inbox",
    response_model=List[schemas.Question])
async def read_user_me_inbox(
        current_user: dict = Depends(get_current_user),
        page: int = 1, per_page: int = 100):
    print(current_user, current_user['sub'])
    user = User.get_or_none(User.link == current_user['sub'])

    if current_user is None or user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    inbox = user.inbox.select()

    questions = inbox.order_by(
        Question.created.desc()
    ).paginate(page, per_page)

    return questions


@app.get(
    "/users/{user_link}/inbox",
    response_model=List[schemas.Question])
async def read_user_inbox(
        user_link: str, page: int = 1, per_page: int = 10):
    user = User.get_or_none(User.link == user_link)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    inbox = user.inbox.select().where(Question.answer.is_null(False))

    questions = inbox.order_by(
        Question.created.desc()
    ).paginate(page, per_page)

    return questions


@app.get(
    "/users/me/outbox",
    response_model=List[schemas.Question])
async def read_user_me_outbox(
        current_user: dict = Depends(get_current_user),
        page: int = 1, per_page: int = 100):
    user = User.get_or_none(User.link == current_user['sub'])

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    outbox = user.outbox.select()

    questions = outbox.order_by(
        Question.created.desc()
    ).paginate(page, per_page)

    return questions


@app.post(
    "/users/{user_link}/inbox",
    response_model=schemas.QuestionCreateResponse)
async def add_question_to_inbox(
        user_link: str,
        question: schemas.QuestionCreate,
        current_user: dict = Depends(get_current_user)):
    sender = User.get_or_none(User.link == current_user['sub'])
    to = User.get_or_none(User.link == user_link)

    if sender is None or to is None:
        print(sender is None, to is None)
        raise HTTPException(status_code=404, detail="User not found")

    question = Question.create(
        sender=sender,
        to=to,
        text=question.text,
        status=0)

    return question


@app.patch(
    "/questions/{question_link}/answer",
    response_model=schemas.Question)
async def answer_question(
        question_link: str,
        data: schemas.QuestionAnswer,
        current_user: dict = Depends(get_current_user)):
    current_user_obj = User.get_or_none(User.link == current_user['sub'])
    question = Question.get_or_none(Question.link == question_link)

    if current_user_obj is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")

    if question.to != current_user_obj:
        raise HTTPException(status_code=403, detail="Forbidden")

    question.answer = data.answer
    question.status = 1
    question.save()
    return question


@app.delete("/questions/{question_link}")
async def delete_question(
        question_link: str,
        current_user: dict = Depends(get_current_user)):
    to = User.get_or_none(User.link == current_user['sub'])
    question = Question.get_or_none(Question.link == question_link)

    if to is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")

    if question.to != to:
        raise HTTPException(status_code=403, detail="Forbidden")

    question.delete_instance()

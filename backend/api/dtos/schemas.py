from datetime import datetime

from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    telegram_id: Optional[int]
    first_name: str
    last_name: Optional[str]
    username: Optional[str]
    link: str

    class Config:
        from_attributes = True


class QuestionBase(BaseModel):
    pass


class Question(QuestionBase):
    text: str
    answer: Optional[str]
    link: str
    created: datetime

    class Config:
        from_attributes = True


class QuestionCreate(QuestionBase):
    text: str


class QuestionAnswer(QuestionBase):
    answer: str


class QuestionCreateResponse(QuestionBase):
    link: str
    created: datetime


class MyQuestion(QuestionBase):
    status: int

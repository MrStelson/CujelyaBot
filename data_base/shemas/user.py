from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    fullname: str
    status: str
    id_feedback: int | None = None
    dateTimeFeedback: datetime | None = None


class UserDto(BaseModel):
    id: int
    username: str
    fullname: str
    status: str
    id_feedback: int | None = None
    dateTimeFeedback: datetime | None = None


class UserRelDto(UserDto):
    feedbacks: list["FeedbackDto"]

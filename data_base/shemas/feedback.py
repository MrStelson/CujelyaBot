from datetime import datetime

from pydantic import BaseModel


class Feedback(BaseModel):
    id: int
    dateTimeFeedback: datetime
    status: str
    user_id: int | None = None
    username: str | None = None


class FeedbackAddDto(BaseModel):
    dateTimeFeedback: datetime
    status: str = "available"
    user_id: int | None = None
    username: str | None = None


class FeedbackDto(FeedbackAddDto):
    id: int


class FeedbackRelDto(FeedbackDto):
    user: "UserDto"

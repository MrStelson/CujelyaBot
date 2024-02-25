from datetime import datetime
from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from data_base.database import Base_model


class User(Base_model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    fullname: Mapped[str]
    id_feedback: Mapped[int] = mapped_column(nullable=True)
    dateTimeFeedback: Mapped[datetime] = mapped_column(nullable=True)
    status: Mapped[str]
    feedbacks: Mapped[List["Feedback"]] = relationship(back_populates="user")


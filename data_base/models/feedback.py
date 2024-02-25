from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from data_base.database import Base_model


class Feedback(Base_model):
    __tablename__ = "feedback"

    id: Mapped[int] = mapped_column(primary_key=True)
    dateTimeFeedback: Mapped[datetime] = mapped_column(unique=True)
    status: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=True)
    username: Mapped[str] = mapped_column(nullable=True)
    user: Mapped["User"] = relationship(back_populates="feedbacks")

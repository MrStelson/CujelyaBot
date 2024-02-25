from datetime import datetime, timedelta, date
from typing import List

from sqlalchemy import select, delete, update, func

from config import HOUR_OFFSET
from data_base.database import async_session_factory
from data_base.shemas.feedback import FeedbackAddDto, Feedback, FeedbackDto
from data_base.models.feedback import Feedback as ORMFeedback


class FeedbackRepositoryImplementation:
    """Класс репозитория консультаций"""

    @staticmethod
    async def create_feedback(feedback_add_dto: FeedbackAddDto):
        """
        Метод создания консультации

        Args:
            feedback_add_dto (FeedbackAddDto): Объект обмена данными о создании консультации

        Returns:

        """
        async with async_session_factory() as session:
            session.add(ORMFeedback(**feedback_add_dto.model_dump()))
            await session.commit()

    @staticmethod
    async def get_all_feedbacks() -> List[Feedback]:
        """
        Метод получения всех консультаций

        Returns:
            List[Feedback]: Список всех консультаций
        """
        async with async_session_factory() as session:
            query = select(ORMFeedback).order_by(ORMFeedback.dateTimeFeedback)
            result = await session.execute(query)
            feedbacks = result.scalars().all()

            return [
                Feedback.model_validate(user, from_attributes=True)
                for user in feedbacks
            ]

    @staticmethod
    async def get_all_booked_success_feedbacks() -> List[Feedback]:
        """
        Метод получения всех забронированных и подтвержденных

        Returns:
            List[Feedback]: Список всех консультаций
        """
        async with async_session_factory() as session:
            query = (
                select(ORMFeedback)
                .filter(ORMFeedback.status.in_(("booked", "success")))
                .order_by(ORMFeedback.dateTimeFeedback)
            )
            result = await session.execute(query)
            feedbacks = result.scalars().all()

            return [
                Feedback.model_validate(user, from_attributes=True)
                for user in feedbacks
            ]

    @staticmethod
    async def delete_feedback(feedback_id: int) -> Feedback:
        """
        Метод удаления консультации

        Args
            feedback_id (int): Идентификатор консультации

        Returns:
            Feedback: Удаленная консультаций
        """
        async with async_session_factory() as session:
            feedback_orm = await session.get(ORMFeedback, feedback_id)
            stmt = delete(ORMFeedback).filter(ORMFeedback.id == feedback_id)
            await session.execute(stmt)
            await session.commit()

            return Feedback.model_validate(feedback_orm, from_attributes=True)

    @staticmethod
    async def update_feedback_status(
        feedback_id: int, status: str, user_id: int | None = None
    ) -> Feedback:
        """
        Метод обновления статуса консультации

        Args:
            feedback_id (int): Идентификатор консультации
            status (str): Новый статус консультации
            user_id (int): Идентификатор пользователя. Defaults to None

        Returns:
            Feedback: Консультация
        """
        async with async_session_factory() as session:
            stmt = (
                update(ORMFeedback)
                .filter(ORMFeedback.id == feedback_id)
                .values(status=status)
            )

            if user_id is not None:
                stmt.values(user_id=user_id)

            await session.execute(stmt)
            await session.commit()

            feedback_orm = await session.get(ORMFeedback, feedback_id)

            return Feedback.model_validate(feedback_orm, from_attributes=True)

    @staticmethod
    async def delete_last_feedbacks() -> None:
        """
        Метод удаления всех прошедших консультаций

        Returns:
            None
        """
        async with async_session_factory() as session:
            datetime_now = datetime.now() - timedelta(hours=HOUR_OFFSET)
            stmt = delete(ORMFeedback).filter(
                ORMFeedback.dateTimeFeedback < datetime_now
            )
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def get_all_active_feedback() -> List[Feedback]:
        """
        Метод получения всех активных консультаций

        Returns:
            List[Feedback]: Список всех консультаций
        """
        async with async_session_factory() as session:
            datetime_now = datetime.now() - timedelta(hours=HOUR_OFFSET)
            query = (
                select(ORMFeedback)
                .filter(ORMFeedback.dateTimeFeedback >= datetime_now)
                .order_by(ORMFeedback.dateTimeFeedback)
            )
            result = await session.execute(query)
            feedbacks = result.scalars().all()

            return [
                Feedback.model_validate(user, from_attributes=True)
                for user in feedbacks
            ]

    @staticmethod
    async def get_feedbacks_by_date(feedback_date: date) -> List[Feedback]:
        """
        Метод получения консультация за определенный день

        Args:
            feedback_date (date): День консультации

        Returns:
            List[Feedback]: Список консультаций
        """
        async with async_session_factory() as session:
            query = (
                select(ORMFeedback)
                .filter(func.date(ORMFeedback.dateTimeFeedback) == feedback_date)
                .order_by(ORMFeedback.dateTimeFeedback)
            )
            result = await session.execute(query)
            feedbacks = result.scalars().all()

            return [
                Feedback.model_validate(feedback, from_attributes=True)
                for feedback in feedbacks
            ]

    @staticmethod
    async def get_feedback_by_datetime(feedback_datetime: datetime) -> Feedback:
        """
        Метод получения консультации по дате и времени

        Args:
            feedback_datetime (datetime): Дата и время консультации

        Returns:
            Feedback: Консультация
        """
        async with async_session_factory() as session:
            query = select(ORMFeedback).filter(
                ORMFeedback.dateTimeFeedback == feedback_datetime
            )
            result = await session.execute(query)
            feedback = result.scalar_one()

            return Feedback.model_validate(feedback, from_attributes=True)

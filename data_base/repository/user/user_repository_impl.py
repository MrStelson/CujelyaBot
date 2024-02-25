from typing import List

from sqlalchemy import select, update

from data_base.database import async_session_factory
from data_base.models.user import User as ORMUser
from data_base.shemas.user import User, UserDto


class UserRepositoryImplementation:
    """Класс репозитория пользователей"""

    @staticmethod
    async def get_user_by_id(user_id: int) -> User | None:
        """
        Метод получения пользователя по идентификатору

        Args:
            user_id (int): Идентификатор пользователя

        Returns:
            User | None: Пользователь
        """
        async with async_session_factory() as session:
            user = await session.get(ORMUser, user_id)

            if user:
                return User.model_validate(user, from_attributes=True)

            return None

    @staticmethod
    async def get_all_user() -> List[User]:
        """
        Метод получения всех пользователей

        Returns:
            List[User]: Список пользователей
        """
        async with async_session_factory() as session:
            query = select(ORMUser)
            result = await session.execute(query)
            users = result.scalars().all()

            return [User.model_validate(user, from_attributes=True) for user in users]

    @staticmethod
    async def get_or_create_user(user: UserDto) -> User:
        """
        Метод создания пользователя

        Args:
            user (UserDto): Сущность обмена данным пользователя

        Returns
            User: Пользователь
        """
        async with async_session_factory() as session:
            user_orm = await session.get(ORMUser, user.id)

            if not user_orm:
                session.add(ORMUser(**user.model_dump()))
                await session.commit()
                user_orm = await session.get(ORMUser, user.id)

            return User.model_validate(user_orm, from_attributes=True)

    @staticmethod
    async def update_user_status(user_id: int, status: str) -> User:
        """
        Метод обновления статуса пользователя

        Args:
            user_id (int): Идентификатор пользователя
            status (str): Новый статус пользователя

        Returns:
            User: Пользователь
        """
        async with async_session_factory() as session:
            stmt = update(ORMUser).filter(ORMUser.id == user_id).values(status=status)

            await session.execute(stmt)
            await session.commit()

            user_orm = await session.get(ORMUser, user_id)

            return User.model_validate(user_orm, from_attributes=True)

    @staticmethod
    async def update_user(user_dto: UserDto) -> User:
        """
        Метод обновления пользователя

        Args:
            user_dto (UserDto): Сущность обмена данным пользователя

        Returns:
            User: Пользователь
        """
        async with async_session_factory() as session:
            stmt = update(ORMUser).values(user_dto.model_dump())

            await session.execute(stmt)
            await session.commit()

            return User.model_validate(
                await session.get(ORMUser, user_dto.id), from_attributes=True
            )

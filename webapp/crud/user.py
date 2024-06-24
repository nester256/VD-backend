from typing import Optional

from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.schema.auth.user import UserRegister
from webapp.models.sirius.user import User
from webapp.logger import logger


async def get_user(session: AsyncSession, user_id: int) -> User | None:
    return (
        await session.scalars(
            select(User).where(
                User.id == user_id
            )
        )
    ).one_or_none()


async def check_user(session: AsyncSession, user_id: int) -> bool:
    query = select(exists().where(User.id == user_id))
    return bool(await session.scalar(query))


async def create_user(session: AsyncSession, user_info: UserRegister) -> Optional[User]:
    try:
        user = User(
            id=user_info.id
        )
        session.add(user)
        await session.commit()
        return user
    except Exception as err:
        logger.error(f'An error occurred while creating a user: {err}')
        await session.rollback()
        return None

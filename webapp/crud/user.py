from typing import Optional

from sqlalchemy import exists, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.logger import logger
from webapp.models.sirius.user import User
from webapp.schema.auth.user import UserRegister


async def get_user(session: AsyncSession, user_id: int) -> User | None:
    return (await session.scalars(select(User).where(User.id == user_id))).one_or_none()


async def check_user(session: AsyncSession, user_id: int) -> bool:
    query = select(exists().where(User.id == user_id))
    return bool(await session.scalar(query))


async def create_user(session: AsyncSession, user_info: UserRegister) -> Optional[User]:
    try:
        user = User(id=user_info.id)
        session.add(user)
        await session.commit()
        return user
    except IntegrityError as err:
        logger.error(f'An error occurred while creating a user: {err}')
        await session.rollback()
        return None

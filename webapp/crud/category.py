from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.integrations.metrics.metrics import async_integrations_timer
from webapp.models.sirius.category import Category


@async_integrations_timer
async def get_categories_page(session: AsyncSession, offset: int, limit: int) -> Sequence[Category]:
    return (await session.scalars(select(Category).limit(limit).offset(offset).order_by(Category.id))).all()

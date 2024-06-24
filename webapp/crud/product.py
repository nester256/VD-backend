from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.integrations.metrics.metrics import async_integrations_timer
from webapp.models.sirius.product import Product


@async_integrations_timer
async def get_products_page(session: AsyncSession, offset: int, limit: int, cat_id: int) -> Sequence[Product]:
    return (
        await session.scalars(
            select(Product)
            .where(Product.category_id == cat_id)
            .limit(limit)
            .offset(offset)
            .order_by(Product.id)
        )
    ).all()


@async_integrations_timer
async def get_product_by_id(session: AsyncSession, id: int):
    return (
        await session.scalars(
            select(Product)
            .where(Product.id == id)
        )
    ).one_or_none()

from sqlalchemy.ext.asyncio import AsyncSession

from webapp.models.sirius.order import Order, StatusEnum
from webapp.models.sirius.order_product import OrderProduct
from webapp.schema.info.order import OrderProductCreate


async def create_order_and_add_products(
        session: AsyncSession,
        user_id: int,
        products: dict[int, int]
) -> Order:
    new_order = Order(user_id=user_id, status=StatusEnum.awaiting_delivery)
    session.add(new_order)
    await session.flush()

    for product_id, quantity in products.items():
        order_product = OrderProduct(order_id=new_order.id, product_id=product_id, quantity=quantity)
        session.add(order_product)

    await session.commit()
    await session.refresh(new_order)  # Refresh to get the updated state of the order

    return new_order
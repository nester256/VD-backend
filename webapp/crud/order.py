from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.models.sirius.order import Order, StatusEnum
from webapp.models.sirius.order_product import OrderProduct
from webapp.models.sirius.product import Product


async def create_order_and_add_products(session: AsyncSession, user_id: int, products: dict[int, int]) -> Order:
    new_order = Order(user_id=user_id, status=StatusEnum.awaiting_delivery)
    session.add(new_order)
    await session.flush()

    for product_id, quantity in products.items():
        order_product = OrderProduct(order_id=new_order.id, product_id=product_id, quantity=quantity)
        session.add(order_product)

    await session.commit()
    await session.refresh(new_order)

    return new_order


async def get_orders_with_total_cost(session: AsyncSession, user_id: int) -> list:
    stmt = (
        select(Order.id, Order.status, func.sum(Product.price * OrderProduct.quantity).label('total_cost'))
        .join(OrderProduct, Order.id == OrderProduct.order_id)
        .join(Product, OrderProduct.product_id == Product.id)
        .where(Order.user_id == user_id)
        .group_by(Order.id)
    )

    result = await session.execute(stmt)
    orders_with_cost = result.fetchall()

    return [
        {'order_id': order.id, 'status': order.status, 'total_cost': round(float(order.total_cost), 2)}
        for order in orders_with_cost
    ]


async def get_orders_to_delivery(session: AsyncSession) -> list:
    stmt = (
        select(Order.id, Product.name, OrderProduct.quantity)
        .join(OrderProduct, Order.id == OrderProduct.order_id)
        .join(Product, OrderProduct.product_id == Product.id)
        .where(Order.status == StatusEnum.awaiting_delivery)
    )

    result = await session.execute(stmt)
    orders_to_delivery = result.fetchall()

    orders_dict = {}
    for order_id, product_name, quantity in orders_to_delivery:
        if order_id not in orders_dict:
            orders_dict[order_id] = {'order_id': order_id, 'products': []}
        orders_dict[order_id]['products'].append({'product_name': product_name, 'quantity': quantity})

    return list(orders_dict.values())


async def set_deliverer(session: AsyncSession, order_id: int, deliverer_id: int) -> bool:
    order = await session.get(Order, order_id)
    if order is not None:
        order.deliverer_id = deliverer_id
        order.status = StatusEnum.delivered
        await session.commit()
        return True
    return False


async def set_order_done(session: AsyncSession, order_id: int) -> bool:
    order = await session.get(Order, order_id)
    if order is not None:
        order.status = StatusEnum.done
        await session.commit()
        return True
    return False


async def get_active_orders(session: AsyncSession, user_id: int) -> list:
    stmt = (
        select(Order.id, Product.name, OrderProduct.quantity)
        .join(OrderProduct, Order.id == OrderProduct.order_id)
        .join(Product, OrderProduct.product_id == Product.id)
        .where(Order.status == StatusEnum.delivered, Order.deliverer_id == user_id)
    )

    result = await session.execute(stmt)
    orders_to_delivery = result.fetchall()

    orders_dict = {}
    for order_id, product_name, quantity in orders_to_delivery:
        if order_id not in orders_dict:
            orders_dict[order_id] = {'order_id': order_id, 'products': []}
        orders_dict[order_id]['products'].append({'product_name': product_name, 'quantity': quantity})

    return list(orders_dict.values())

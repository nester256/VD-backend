from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, List

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship

from webapp.models.meta import DEFAULT_SCHEMA, Base

if TYPE_CHECKING:
    from webapp.models.sirius.product import Product
    from webapp.models.sirius.user import User


class StatusEnum(Enum):
    awaiting_payment = 'awaiting_payment'
    awaiting_delivery = 'awaiting_delivery'
    delivered = 'delivered'
    done = 'done'


class Order(Base):
    __tablename__ = 'order'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('user.id'))

    deliverer_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('user.id'), nullable=True)

    user: Mapped['User'] = relationship(
        'User', back_populates='orders', foreign_keys='Order.user_id', uselist=False, overlaps='deliverer'
    )

    deliverer: Mapped['User'] = relationship('User', foreign_keys='Order.deliverer_id', overlaps='orders')

    create: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    status: Mapped[StatusEnum] = mapped_column(ENUM(StatusEnum, inherit_schema=True))

    products: Mapped[List['Product']] = relationship(
        secondary=f'{DEFAULT_SCHEMA}.order_product',
        back_populates='orders',
    )

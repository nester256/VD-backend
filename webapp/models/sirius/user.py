from enum import Enum
from typing import TYPE_CHECKING, List
from sqlalchemy import Integer, String, BigInteger
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship

from webapp.models.meta import Base

if TYPE_CHECKING:
    from webapp.models.sirius.order import Order


class UserRoleEnum(Enum):
    admin = 'admin'
    deliverer = 'deliverer'
    customer = 'customer'


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    address: Mapped[str] = mapped_column(String, nullable=True)

    role: Mapped[UserRoleEnum] = mapped_column(ENUM(UserRoleEnum), default=UserRoleEnum.customer)

    orders: Mapped[List['Order']] = relationship('Order', back_populates='user', foreign_keys='Order.user_id', overlaps="deliveries")

    deliveries: Mapped[List['Order']] = relationship('Order', foreign_keys='Order.deliverer_id', overlaps="deliverer")

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

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    username: Mapped[int] = mapped_column(BigInteger, unique=True)

    tg: Mapped[str] = mapped_column(String)

    code: Mapped[str] = mapped_column(String)

    address: Mapped[str] = mapped_column(String)

    role: Mapped[UserRoleEnum] = mapped_column(ENUM(UserRoleEnum))

    orders: Mapped[List['Order']] = relationship('Order', back_populates='user')

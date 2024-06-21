from decimal import Decimal
from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey, Integer, String, Index, DECIMAL, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from webapp.models.meta import Base, DEFAULT_SCHEMA

if TYPE_CHECKING:
    from webapp.models.sirius.order import Order
    from webapp.models.sirius.category import Category


class Product(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    name: Mapped[str] = mapped_column(String, nullable=False)

    description: Mapped[str] = mapped_column(String, nullable=False)

    price: Mapped[Decimal] = mapped_column(DECIMAL, nullable=False)

    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('category.id'), nullable=False)

    category: Mapped['Category'] = relationship('Category', back_populates='products')

    picture_url: Mapped[str] = mapped_column(Text, nullable=True)

    orders: Mapped[List['Order']] = relationship(
        secondary=f'{DEFAULT_SCHEMA}.order_product',
        back_populates='products',
    )


product_index = Index('product_index', Product.name, postgresql_using='btree')

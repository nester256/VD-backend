from typing import Dict, List

from pydantic import BaseModel, ConfigDict

from webapp.models.sirius.order import StatusEnum


class OrderProductCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    product_id: int
    quantity: int


class CreateOrderRequest(BaseModel):
    products: Dict[int, int]


class CreateOrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    order_id: int
    status: StatusEnum


class OrderWithTotalCost(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    order_id: int
    status: StatusEnum
    total_cost: float


class OrdersListResponse(BaseModel):
    orders: List[OrderWithTotalCost]

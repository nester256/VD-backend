from pydantic import BaseModel, ConfigDict


class ProductResp(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    price: float


class ProductsPageResp(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    products: list[ProductResp]


class ProductInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    description: str
    price: float
    category_id: int
    picture_url: str | None

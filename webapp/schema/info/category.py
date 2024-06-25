from pydantic import BaseModel, ConfigDict


class CategoryResp(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str


class CategoriesPageResp(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    categories: list[CategoryResp]

from fastapi import APIRouter

from webapp.api.v1.auth.router import auth_router
from webapp.api.v1.categories.router import categories_router
from webapp.api.v1.products.router import products_router

v1_router = APIRouter(prefix='/api/v1')

v1_router.include_router(auth_router, prefix='/auth', tags=['AUTH API'])
v1_router.include_router(categories_router, prefix='/categories', tags=['CATS API'])
v1_router.include_router(products_router, prefix='/products', tags=['PROD API'])

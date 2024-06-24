from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.v1.products.router import products_router
from webapp.crud.product import get_products_page, get_product_by_id
from webapp.db.postgres import get_session
from webapp.logger import logger
from webapp.schema.info.product import ProductsPageResp, ProductInfo
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@products_router.get('', response_model=ProductsPageResp)
async def get_products(
        offset: int,
        limit: int,
        cat_id: int,
        access_token: JwtTokenT = Depends(jwt_auth.validate_token),
        session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    try:
        products = await get_products_page(session, offset, limit, cat_id)
        if not products:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        serialized_prds = {'products': products}
        return ORJSONResponse(
            content=ProductsPageResp.model_validate(serialized_prds).model_dump(),
            status_code=status.HTTP_200_OK
        )
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        logger.error(f'An error occurred while verifying login information: {e}')
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)


@products_router.get('/product', response_model=ProductInfo)
async def get_product(
        id: int,
        access_token: JwtTokenT = Depends(jwt_auth.validate_token),
        session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    try:
        product = await get_product_by_id(session, id)
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return ORJSONResponse(
            content=ProductInfo.model_validate(product).model_dump(),
            status_code=status.HTTP_200_OK
        )
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        logger.error(f'An error occurred while verifying login information: {e}')
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

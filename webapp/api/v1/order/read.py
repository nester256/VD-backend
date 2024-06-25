from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.v1.order.router import orders_router
from webapp.crud.order import get_active_orders, get_orders_to_delivery, get_orders_with_total_cost
from webapp.db.postgres import get_session
from webapp.logger import logger
from webapp.schema.info.order import OrdersListResponse
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@orders_router.get('/list', response_model=OrdersListResponse)
async def get_orders(
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    try:
        user_id = access_token.get('user_id')
        orders_with_cost = await get_orders_with_total_cost(session, user_id)
        return ORJSONResponse(content={'orders': orders_with_cost}, status_code=status.HTTP_200_OK)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        logger.error(f'An error occurred while fetching orders: {e}')
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)


@orders_router.get('/list_to_delivery', response_model=OrdersListResponse)
async def get_to_delivery_orders(
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    try:
        orders_with_products = await get_orders_to_delivery(session)
        return ORJSONResponse(content={'orders': orders_with_products}, status_code=status.HTTP_200_OK)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        logger.error(f'An error occurred while fetching orders: {e}')
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)


@orders_router.get('/list_active', response_model=OrdersListResponse)
async def get_deliverer_orders(
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    try:
        user_id = access_token.get('user_id')
        print(user_id)
        orders_with_products = await get_active_orders(session, user_id)
        return ORJSONResponse(content={'orders': orders_with_products}, status_code=status.HTTP_200_OK)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        logger.error(f'An error occurred while fetching orders: {e}')
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

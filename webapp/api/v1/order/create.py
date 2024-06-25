from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.v1.order.router import orders_router
from webapp.crud.order import create_order_and_add_products
from webapp.db.postgres import get_session
from webapp.logger import logger
from webapp.schema.info.order import CreateOrderRequest, CreateOrderResponse
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@orders_router.post('/create')
async def create_order(
    order_request: CreateOrderRequest,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    try:
        if order_request:
            user_id = access_token.get('user_id')
            new_order = await create_order_and_add_products(session, user_id, order_request.products)

            return ORJSONResponse(
                content=CreateOrderResponse(order_id=new_order.id, status=new_order.status).model_dump(),
                status_code=status.HTTP_201_CREATED,
            )
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        logger.error(f'An error occurred while creating the order: {e}')
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

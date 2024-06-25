from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.v1.order.router import orders_router
from webapp.crud.order import set_deliverer, set_order_done
from webapp.db.postgres import get_session
from webapp.logger import logger
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@orders_router.get('/create_delivery/{order_id}')
async def create_delivery(
    order_id: int,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    try:
        user_id = access_token.get('user_id')
        res = await set_deliverer(session, order_id, user_id)
        if res:
            return ORJSONResponse(status_code=status.HTTP_200_OK, content='success')
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    except HTTPException as http_err:
        print(http_err)
        raise http_err
    except Exception as e:
        print(e)
        logger.error(f'An error occurred while set order delivery: {e}')
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)


@orders_router.get('/delivery_done/{order_id}')
async def delivery_done(
    order_id: int,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    try:
        res = await set_order_done(session, order_id)
        if res:
            return ORJSONResponse(status_code=status.HTTP_200_OK, content='success')
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        logger.error(f'An error occurred while set order done: {e}')
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

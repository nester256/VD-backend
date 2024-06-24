from fastapi import Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.v1.auth.router import auth_router
from webapp.crud.user import check_user, create_user
from webapp.db.postgres import get_session
from webapp.schema.auth.user import UserRegister
from webapp.logger import logger


@auth_router.post("/register")
async def auth_register_handler(
        body: UserRegister,
        session: AsyncSession = Depends(get_session),
) -> Response:
    try:
        user_exists = await check_user(session, body.id)

        if user_exists:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT)

        new_user = await create_user(session, body)
        if new_user is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

        return Response(status_code=status.HTTP_201_CREATED)
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        logger.error(f'An error occurred during registration: {e}')
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)

from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.v1.categories.router import categories_router
from webapp.crud.category import get_categories_page
from webapp.db.postgres import get_session
from webapp.logger import logger
from webapp.schema.info.category import CategoriesPageResp
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@categories_router.get('', response_model=CategoriesPageResp)
async def get_categories(
    offset: int,
    limit: int,
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    try:
        categories = await get_categories_page(session, offset, limit)
        if not categories:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        serialized_cats = {'categories': categories}
        return ORJSONResponse(
            content=CategoriesPageResp.model_validate(serialized_cats).model_dump(), status_code=status.HTTP_200_OK
        )
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        logger.error(f'An error occurred while verifying login information: {e}')
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

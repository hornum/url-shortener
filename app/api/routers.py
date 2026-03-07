import datetime
import string
import secrets

from fastapi import APIRouter, Query, HTTPException
from sqlalchemy import select
from starlette.responses import RedirectResponse, JSONResponse

from app.models.links import LinkModel
from app.db.session import async_session_maker

from app.schemas.links import LinkInfo


ALPHABET = string.ascii_letters + string.digits

def generate_random_string():
    return ''.join(secrets.choice(ALPHABET) for i in range(8))

router = APIRouter(prefix="/links", tags=["Links"])
@router.post('/')
async def shorten_link(link: str = Query(min_length=3)) -> str:
    async with async_session_maker() as session:
        new_link = LinkModel(
            long_url=link,
            short_url=generate_random_string(),
            used_count=0,
            created_at=datetime.datetime.now(),
        )
        session.add(new_link)
        await session.commit()
        return f'http://127.0.0.1:8000/links/{new_link.short_url}'

@router.get('/{short_link}')
async def get_long_link(short_link: str) -> RedirectResponse:
    async with (async_session_maker() as session):
        result = await session.execute(
            select(LinkModel).where(LinkModel.short_url == short_link)
        )
        link = result.scalar_one_or_none()

        if not link:
            raise HTTPException(status_code=404, detail="Link not found")

        link.used_count += 1
        await session.commit()

        return RedirectResponse(url=link.long_url)

@router.get('/info/{short_link}', response_model=LinkInfo)
async def shorten_link(short_link: str) -> LinkInfo:
    async with async_session_maker() as session:
        result = await session.execute(
            select(LinkModel).where(LinkModel.short_url == short_link)
        )
        link = result.scalar_one_or_none()
        if not link:
            raise HTTPException(status_code=404, detail="Link not found")
        info = LinkInfo(
            link_id=link.id,
            short_link=f'http://127.0.0.1:8000/links/{link.short_url}',
            long_link=link.long_url,
            used_count=link.used_count,
            created_at=link.created_at,
        )
        return info
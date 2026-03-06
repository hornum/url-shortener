from fastapi import APIRouter

from app.models.links import MakeShortModel

router = APIRouter(prefix="/links", tags=["Links"])

@router.post('/')
async def shorten_link(link: MakeShortModel):
    pass

@router.get('/{short_link}')
async def get_long_link(short_link: str):
    pass

@router.get('/{short_link}/info')
async def shorten_link(short_link: str):
    pass
import datetime

from pydantic import BaseModel

class LinkInfo(BaseModel):
    id: int
    short_link: str
    long_link: str
    used_count: int
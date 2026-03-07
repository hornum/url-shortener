from datetime import datetime

from pydantic import BaseModel

class LinkInfo(BaseModel):
    link_id: int
    short_link: str
    long_link: str
    used_count: int
    created_at: datetime
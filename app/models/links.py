from sqlalchemy import Column, Integer, String, DateTime
import datetime

from app.db.session import Base

class MakeShortModel(Base):
    __tablename__ = 'Links'

    id = Column(Integer, primary_key=True)
    short_url = Column(String, unique=True, nullable=False)
    long_url = Column(String, unique=True, nullable=False)
    used_count = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.datetime.now())
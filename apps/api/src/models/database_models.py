from database import Base
from sqlalchemy import Column, String, DateTime, Integer
from datetime import datetime, UTC

class JobModel(Base):
    __tablename__ = "jobs"
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String)
    title = Column(String, index=True)
    company = Column(String)
    location = Column(String)
    description = Column(String)
    summary = Column(String)
    skills = Column(String, nullable=True)
    yoe = Column(String, nullable=True)
    benefits = Column(String, nullable=True)
    url = Column(String, nullable=True)
    min_salary = Column(Integer, nullable=True)
    max_salary = Column(Integer, nullable=True)
    currency = Column(String, nullable=True)
    rate = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    applied_at = Column(DateTime, default=lambda: datetime.now(UTC))
    class Config:
        from_attributes = True
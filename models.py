import os

from sqlalchemy import Column, DateTime, Integer, String, Text, ForeignKey, func
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

PG_USER = os.getenv("PG_USER", "username")
PG_PASSWORD = os.getenv("PG_PASSWORD", "1111")
PG_DB = os.getenv("PG_DB", "aiohttp")
PG_HOST = os.getenv("PG_HOST", "127.0.0.1")
PG_PORT = os.getenv("PG_PORT", "5220")

PG_DSN = f"postgresql+asyncpg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"

engine = create_async_engine(PG_DSN)
Base = declarative_base()
Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    creation_time = Column(DateTime, server_default=func.now())

class Ads(Base):
    __tablename__ = "Ads"

    id = Column(Integer, primary_key=True)
    title = Column(String,nullable=False)
    description = Column(Text)
    creation_time = Column(DateTime, server_default=func.now())
    user_id = Column(Integer, ForeignKey("User.id"), nullable=False)

    owner = relationship(User, backref="Ads")
import asyncio
from typing import AsyncIterable, TypeVar

from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.settings import load_setting

SessionFactory = TypeVar("SessionFactory")


# def create_engine(url) -> AsyncEngine:
#     return create_async_engine(url, echo=True)
#
#
# def create_as_session_maker(engine: AsyncEngine) -> SessionFactory:
#     return async_sessionmaker(engine, expire_on_commit=False)
engine = create_async_engine(load_setting().db_setting.get_url, echo=True)

async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session


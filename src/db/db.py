from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.setting import settings

engine = create_async_engine(settings.db_dsn, echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session():
    async with async_session_maker() as session:
        yield session

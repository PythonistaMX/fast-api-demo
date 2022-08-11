from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from settings import SQLALCHEMY_DATABASE_URL

engine = create_async_engine(SQLALCHEMY_DATABASE_URL)

session = sessionmaker(engine, 
                            expire_on_commit=False, 
                            class_=AsyncSession)

async def get_db():
    with session() as db:
        print(db)
        await db
import pytest
# import asyncio
from fastapi.testclient import TestClient
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker, AsyncConnection
# from sqlalchemy.orm import declarative_base

# from src.app.database import Base
from src.app.main import app


@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client


# DATABASE_URL = "postgresql+asyncpg://postgres:12345@localhost/fadb_test"


# # 1. Session-scoped event loop (required for session-scoped async fixtures)
# @pytest.fixture(scope="session")
# def event_loop():
#     """Creates an instance of the default event loop for the test session."""
#     loop = asyncio.new_event_loop()
#     yield loop
#     loop.close()


# # 2. Session-scoped async engine
# @pytest.fixture(scope="session")
# async def async_engine():
#     """Creates an asynchronous database engine."""
#     engine = create_async_engine(DATABASE_URL, echo=True)
#     yield engine
#     await engine.dispose()


# # 3. Session-scoped fixture to create/drop tables
# @pytest.fixture(scope="session", autouse=True)
# async def setup_database(async_engine):
#     """Creates all tables before tests and drops them after."""
#     async with async_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#     yield
#     async with async_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)

# # 4. Function-scoped async database session for transactional tests
# @pytest.fixture(scope="function")
# async def async_db_session(async_engine):
#     """Provides a transactional isolation for each test function."""
#     connection = await async_engine.connect()
#     # Begin a transaction (or nested transaction for complex setups)
#     trans = await connection.begin()

#     # Create an AsyncSession fully bound to the connection
#     async_session = async_sessionmaker(connection, expire_on_commit=False, class_=AsyncSession)
#     session = async_session()

#     yield session

#     # Roll back the transaction and close the connection after the test
#     await trans.rollback()
#     await connection.close()

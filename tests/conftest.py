import asyncio
import pytest_asyncio
import pytest

from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from main import app
from src.entity.models import Base, User
from src.database.db import get_db
from src.services.auth import auth_service


SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = async_sessionmaker(
    autocommit=False, autoflush=False, expire_on_commit=False, bind=engine
)

test_user = {"username": "test", "email": "test@test.com", "password": "123456789"}


@pytest.fixture(scope="module", autouse=True)
def init_models_wrap():
    async def init_models():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        async with TestingSessionLocal() as session:
            hash_password = auth_service.get_password_hash(test_user["password"])
            current_user = User(
                username=test_user["username"],
                email=test_user["email"],
                password=hash_password,
                confirmed=True,
                role="admin",
            )
            session.add(current_user)
            await session.commit()

    asyncio.run(init_models())


@pytest.fixture(scope="module")
def client(init_models_wrap):
    # Dependency override

    async def override_get_db():
        session = TestingSessionLocal()
        try:
            yield session
        except Exception as err:
            print(err)
            await session.rollback()
        finally:
            await session.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

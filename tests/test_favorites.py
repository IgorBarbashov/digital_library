import asyncio
import pytest

from httpx import ASGITransport, AsyncClient
from typing import AsyncGenerator
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker, AsyncConnection
from sqlalchemy.engine import Connection

from src.main import app
from src.setting import settings
from src.db.db import get_async_session
from src.auth.api import get_current_active_user
from src.constants.user_role import UserRole
from src.domains.role.models import Role
from src.domains.user.models import User
from src.domains.user.schema import UserReadSchema
from src.domains.book.models import Book
from src.domains.genre.models import Genre

TEST_DATABASE_URL = settings.db_dsn


@pytest.fixture(scope="session")
async def engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=True, future=True)
    yield engine
    await engine.dispose()

@pytest.fixture(scope="function")
async def db_connection(engine: AsyncEngine) -> AsyncConnection:
    """
    Создаёт соединение с БД и начинает транзакцию.
    После теста — откатывает транзакцию.
    """
    async with engine.begin() as conn:
        yield conn

@pytest.fixture(scope="function")
async def db_session(db_connection: AsyncConnection) -> AsyncSession:
    """
    Создаёт сессию, привязанную к транзакции соединения.
    Все операции будут в одной транзакции.
    """
    session = AsyncSession(bind=db_connection)
    try:
        yield session
    except Exception as e:
        print(f"Ошибка в сессии БД: {e}")
        raise
    finally:
        await session.close()

@pytest.fixture(autouse=True)
async def event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        yield loop
    finally:
        if hasattr(loop, "shutdown_asyncgens"):
            await loop.shutdown_asyncgens()
        loop.close()

def override_get_current_active_user(test_user: User):
    return UserReadSchema(
        id=test_user.id,
        username=test_user.username,
        first_name=test_user.first_name,
        last_name=test_user.last_name,
        email=test_user.email,
        disabled=test_user.disabled,
        role=UserRole.ADMIN,
    )

@pytest.fixture
def client(db_session: AsyncSession, test_user: User) -> AsyncClient:
    def override_get_async_session():
        return db_session

    app.dependency_overrides[get_current_active_user] = lambda: override_get_current_active_user(test_user)
    app.dependency_overrides[get_async_session] = override_get_async_session

    client = AsyncClient(transport=ASGITransport(app=app), base_url="http://test")
    return client

@pytest.fixture
async def test_role(db_session: AsyncSession) -> Role | None:
    try:
        result = await db_session.execute(
            select(Role).where(Role.name == UserRole.ADMIN)
        )
        role = result.scalars().first()
        return role
    except Exception as e:
        print(f"Ошибка в test_role: {e}")
        raise

@pytest.fixture
async def test_user(db_session: AsyncSession, test_role: Role | None) -> User:
    if test_role is None:
        test_role = Role(name=UserRole.ADMIN.value)
        db_session.add(test_role)
        await db_session.flush()  # только flush, без commit!

    user = User(
        username="user1",
        first_name="Test",
        last_name="Testovich",
        email="test@example1.ru",
        disabled=False,
        hashed_password="fakehash",
        role_id=test_role.id,
    )
    db_session.add(user)
    await db_session.flush()  # только flush, без commit
    await db_session.refresh(user)
    return user

@pytest.fixture(scope="function")
async def test_genre(db_session: AsyncSession) -> Genre:
    genre = Genre(name="Genre22")
    db_session.add(genre)
    await db_session.flush()  # только flush
    await db_session.refresh(genre)
    return genre

@pytest.fixture(scope="function")
async def test_book(db_session: AsyncSession, test_genre: Genre) -> Book:
    book = Book(title="Test Book", genre_id=test_genre.id)
    db_session.add(book)
    await db_session.flush()  # только flush
    await db_session.refresh(book)
    return book

@pytest.mark.anyio
async def test_add_book_to_favorites(client: AsyncClient, test_user: User, test_book: Book):
    print(client)
    favorites_data = {"user_id": str(test_user.id), "book_id": str(test_book.id)}

    response = await client.post(
        "/api/v1/favorites/",
        json=favorites_data,
    )

    print("Response status:", response.status_code)
    print("Response body:", response.json())

    assert response.status_code == 201

    # data = response.json()

    # Проверяем поля
    # assert data["book_id"] == str(test_book.id)
    # assert "id" in data
    # assert "user_id" in data


"""
@pytest.mark.asyncio
async def test_list_favorites_with_genres(
    client: TestClient,
    test_user: User,
    test_book: Book,
    test_genre: Genre,
):
    # Добавляем книгу в избранное
    client.post(
        "/favorites/",
        json={"book_id": str(test_book.id)},
    )

    # Получаем список избранных
    response = client.get("/favorites/")
    assert response.status_code == 200
    data = response.json()

    assert len(data) == 1
    favorite = data[0]

    # Проверяем книгу и её жанр
    assert favorite["book"]["id"] == str(test_book.id)
    assert favorite["book"]["title"] == test_book.title
    assert favorite["book"]["genre"]["id"] == str(test_genre.id)
    assert favorite["book"]["genre"]["name"] == test_genre.name

@pytest.mark.asyncio
async def test_delete_favorite(
    client: TestClient,
    test_user: User,
    test_book: Book,
    test_genre: Genre,
):
    # 1. Добавляем книгу в избранное
    response_add = client.post(
        "/favorites/",
        json={"book_id": str(test_book.id)},
    )
    assert response_add.status_code == 201
    favorite_id = response_add.json()["id"]

    # 2. Проверяем, что книга действительно в избранном
    response_list = client.get("/favorites/")
    assert response_list.status_code == 200
    favorites = response_list.json()
    assert len(favorites) == 1
    assert favorites[0]["id"] == favorite_id
    assert favorites[0]["book"]["id"] == str(test_book.id)

    # 3. Удаляем из избранного
    response_delete = client.delete(f"/favorites/{favorite_id}")
    assert response_delete.status_code == 204  # No Content

    # 4. Проверяем, что запись исчезла
    response_list_after = client.get("/favorites/")
    assert response_list_after.status_code == 200
    assert len(response_list_after.json()) == 0
"""

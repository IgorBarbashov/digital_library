### Рекомендации по тестированию для GitHub Copilot

**Общие сведения о проекте и стеке тестов:**

- Бэкенд построен на FastAPI + Pydantic + SQLAlchemy (async).​
- Для тестов используются pytest, pytest-asyncio, httpx.AsyncClient и SQLAlchemy AsyncSession.​
- Все тесты находятся в директории tests/ и повторяют доменную структуру из src/domains/.

**При генерации тестов Copilot должен:**

- Отдавать приоритет асинхронным тестам с @pytest.mark.asyncio.
- Использовать существующие фикстуры и вспомогательные функции из tests/, а не создавать новые подключения к БД или приложению.

**Настройка приложения и базы данных для тестов:**

- ASGI‑приложение импортируется из src.main как app.
- Основная зависимость для асинхронной сессии БД — get_async_session из src.db.db.
- В тестах используется отдельная БД SQLite в памяти с URL: sqlite+aiosqlite:///:memory:.

**Фикстуры из tests/conftest.py, которые нужно всегда переиспользовать:**

- prepare_database (scope session, autouse):
  - создаёт все таблицы через Base.metadata.create_all перед запуском тестов и закрывает engine после.
- db_session:
  - возвращает AsyncSession, привязанную к тестовому engine.
- client:
  - возвращает httpx.AsyncClient, настроенный следующим образом:
    - ASGITransport(app=app)
    - base_url="<http://test>"
    - использование LifespanManager(app) для корректной обработки lifespan‑событий FastAPI.

Запрещается в тестах напрямую создавать engine, session или AsyncClient. Всегда использовать эти фикстуры.

**Аутентификация, пользователи и роли**
Для тестов, где требуется авторизованный пользователь, следует использовать уже существующие фикстуры:

- Роли (tests/role/conftest.py):
  - Фикстура seed_roles (scope function, autouse=True) гарантирует наличие ролей Role с именами "user" и "admin".
  - Не нужно повторно создавать роли в отдельных тестах.
- Пользователи (tests/user/conftest.py):
  - existing_test_user:
    - гарантирует существование тестового пользователя с данными TEST_USER через API (USER_API_BASE_URL), а затем находит его в БД.
    - user_token:
      - логинится через POST на f"{AUTH_API_BASE_URL}login"
      - возвращает словарь:
        - "user_id": UUID существующего пользователя.
        - "token": JSON с токеном доступа.

**При генерации тестов Copilot должен:**

- Использовать user_token для получения access token.
- Не реализовывать повторно логику регистрации/логина в каждом тесте.

**API‑пути и конфигурация**

**Базовые URL для основных доменов определены в tests/config.py:**

- USER_API_BASE_URL = "/api/v1/user/"
- AUTH_API_BASE_URL = "/api/v1/auth/"
- FAVORIYES_API_BASE_URL = "/api/v1/favorites/"

Тесты не должны хардкодить эти пути. Всегда импортировать их из tests.config.

**Доменные фикстуры**

Для подготовки тестовых данных следует использовать доменные conftest.py‑файлы.

**Favorites**
В tests/favorites/conftest.py определены:
    - test_genre(db_session: AsyncSession) -> Genre:
        - Ищет Genre с именем "Test Genre"; если не найден, создаёт, добавляет в сессию и коммитит.
    - test_book(db_session: AsyncSession, test_genre: Genre) -> Book:
        - Ищет Book с заголовком "Test Book"; если не найден, создаёт книгу с genre_id = test_genre.id и коммитит.

При генерации тестов для favorites или связанных с книгами эндпоинтов Copilot должен:
    - Использовать эти фикстуры (test_genre, test_book) для подготовки данных.
    - Не создавать Genre и Book напрямую в теле теста, если это не какой‑то специфичный кейс.

**Роли и другие домены**

Для остальных доменов нужно следовать аналогичному паттерну:
    - Размещать доменные фикстуры в tests/<domain_name>/conftest.py.
    - Переиспользовать общие фикстуры client, db_session, user_token.
    - Все операции с БД выполнять через db_session и не создавать отдельные сессии.

**Стиль и структура тестов**

При генерации тестов FastAPI‑хэндлеров Copilot должен:
    - Размещать тесты домена в tests/<domain_name>/test_<domain_name>.py (например tests/favorites/test_favorites.py).
    - Создавать асинхронные тесты с декоратором @pytest.mark.asyncio.
    - Использовать следующий стиль сигнатур: Имя функции: test_<фича>_<сценарий>
    - Пример для эндпоинта с авторизацией:
        ```python
        @pytest.mark.asyncio
        async def test_add_book_to_favorites(
            client: AsyncClient,
            db_session: AsyncSession,
            user_token: dict[str, Any],
            test_book: Book,
        ) -> None:
            ...
        ```
    - Всегда указывать типы аргументов и -> None как возвращаемый тип.

**Образец паттерна (ориентир)**
Новые тесты для хэндлеров должны следовать такому паттерну (на уровне логики):

1. Подготовка состояния БД через фикстуры и SQLAlchemy:

- Выполнять запрос через:

    ```python
    result = await db_session.execute(select(Model).where(...))
    instance = result.scalars().first()
    ```

1. При необходимости удалить существующие записи, мешающие сценарию:

    ```python
    if instance:
        await db_session.delete(instance)
        await db_session.commit()
    ```

2. HTTP‑запрос через client:

    - Для JSON‑эндпоинтов:

        ```python
        headers = {
            "Authorization": f"Bearer {user_token['token']['access_token']}",
            "Content-Type": "application/json",
        }
        response = await client.post(SOME_API_BASE_URL, headers=headers, json=payload)
        ```

    - Для application/x-www-form-urlencoded:

        ```python
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = await client.post(url, headers=headers, data=form_payload)
        ```

3. Проверки (assert):
    - Всегда явно проверять HTTP‑код:

        ```python
        assert response.status_code == 201
        ```

    - Для JSON‑ответа:

        ```python
        data = response.json()
        assert "user_id" in data
        assert data["book_id"] == str(test_book.id)
        ```

    - По возможности проверять как статус, так и ключевые поля ответа (id, связи, обязательные поля).

4. При необходимости — проверка состояния БД:
    - Убедиться, что запись создана/удалена, связи корректны и нет дубликатов.

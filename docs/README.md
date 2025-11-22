### Архитектура проекта

Разработка проекта ведется в соответствии с принципами `Layered Architecture`

### Файловая структура проекта

```
fastapi-project
├── alembic/
├── docs/
├── src
│   ├── api
│   │   └── v1
│   │       └── init.py
│   ├── db
│   │   └ db.py
│   ├── domains
│   │   ├── author
│   │   │   ├── api.py
│   │   │   ├── models.py
│   │   │   ├── protocols.py
│   │   │   ├── repository.py
│   │   │   ├── schema.py
│   │   │   └── services.py
│   │   ├── genre
│   │   │   ├── api.py
│   │   │   ├── models.py
│   │   │   ├── protocols.py
│   │   │   ├── repository.py
│   │   │   ├── schema.py
│   │   │   └── services.py
│   │   └── common
│   │       ├── association
│   │       │   ├── author_genre.py
│   │       │   └── ...
│   │       ├── models.py
│   │       └── schema.py
│   ├── exceptions
│   │   ├── entity.py
│   │   ├── ...
│   │   └── init.py
│   ├── main.py
│   └── setting.py
├── tests
│   ├── author
│   ├── genre
│   └── ...
├── .env
├── .gitignore
├── .gitlab-ci.yml
├── alembic.ini
├── docker-compose.override.yml
├── docker-compose.yml
├── Dockerfile
├── Makefile
├── poetry.lock
└── pyproject.toml
```

- `/api/v1/init.py` - инициализация всех `API` (подключение роутеров к `app`)
- `/db/db/py` - инициализация подключения к БД, создание и контроль работы с сессиями БД
- `/src/<domain_name>` - содержит директории всех доменных сущностей
    
    Каждая `<domain_name>` папка содержит:
    - `api.py` - контролеры (эндпоинты)
    - `models.py` - `orm`-модели
    - `protocols.py` - протоколы (интерфейсы) репозиториев. Содержат только сигнатуры методов. Не содержат конкретной реализации
    - `repository.py` - имплементация работы с БД средствами `ORM`. Должны наследоваться от протокола
    - `schema.py` - доменные модели, `pydantic`-схемы объектов `dto` и `response`
    - `services.py` - бизнес-логика
- `/src/common` - базовые `orm`-модели и доменные схемы, от которых наследуются все остальные
- `/src/common/association` - содержит файлы для связующих таблиц, реализующих отношения `many-to-many`
- `tests` - `unit`-тесты

### Соглашение об именовании

- названия доменных моделей, `orm`-моделей, таблиц БД, `pydantic`-схем даются в единственном числе
- названия `orm`-моделей (файлы `models.py`) даются без суффиксов (например `Author`, `User`)
- названия доменных моделей (файлы `schema.py`) даются с суффиксом `Schema` (например `UserSchema`, `UserCreateSchema`)
- названия протоколов для репозиториев (файлы `protocols.py`) даются с суффиксом `Repository` (например `AuthorRepository`, `UserRepository`)
- названия классов имплиментирующих логику репозиториев (файлы `repository.py`) даются с суффиксом `Repository` и кратким названием БД (например 
`AuthorRepositoryPG`)
- названия сервисов (файлы `services.py`) даются с суффиксом `Service` (например `AuthorService`, `UserService`)

### Правила импортов

В проекте используются абсолютные импорты

``` python
from src.domains.author.models import Author
from src.domains.genre.models import Genre
```

В проекте не используются файлы `__init__.py` для инициализации модулей и паттерна `PublicAPI`. Импорт должен производиться из конечного файла.

### Преобразование типов данных между архитектурными слоями

### Dependency Injection

### Follow the REST

### FastAPI response serialization

### Обработка исключений

### Запуск проекта

### Создание и запуск миграций

### Контроль качества кода

1. Линтеры, форматтеры
2. Кросс-ревью
3. Тесты

### Логирование

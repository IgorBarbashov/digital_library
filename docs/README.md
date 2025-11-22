### Архитектура проекта

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

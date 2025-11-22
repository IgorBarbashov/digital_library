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

### Соглашения об именовании

### Правила импортов

В проекте используются абсолютные импорты

``` python
from src.domains.author.models import Author
from src.domains.genre.models import Genre
```

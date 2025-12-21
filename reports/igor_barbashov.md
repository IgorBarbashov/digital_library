### Игорь Барбашов, аналитик-разработчик

**Перечень задач с описанием работы**

- Написание кода для обеспечения работы API доменных сущностей Автор, Жанр, Пользователь, Роль. Для каждой сущности были созданы следующие модули:
  - orm-модель
  - pydantic-схемы
  - api handlers
  - методы слоя для работы с БД (repository, при необходимости)
  - тесты
- Написание кода для обеспечения работы Личного кабинета пользователя, защищенного авторизацией
- Инициализация приложения: старт приложения, инициализация роутинга, настройка глобальных Exception handlers
- Определение файловой структры приложения учитывая требования Layered architecture
- Настройка Alembic, автоматизации применения миграций
- Создание модуля авторизации + служебные методы безопасности
- Создание и конфигурирование тестового окружения
- Написание документации проекта
- Декомпозиция задач
- Проведение ревью MR других разработчиков команды

**Перечень задач на доске и merge requests**

| Задача | Ссылка на доску | Ссылка на MR |
|---|---|---|
| Добавить себя в авторы проекта | [Task](https://gitlab.com/miptfastapiproject/fastapi-project/-/issues/4) | [Merge request](https://gitlab.com/miptfastapiproject/fastapi-project/-/merge_requests/8) |
| Создать ORM модель Author | [Task](https://gitlab.com/miptfastapiproject/fastapi-project/-/issues/6) | [Merge request](https://gitlab.com/miptfastapiproject/fastapi-project/-/merge_requests/11) |
| Разработать API для работы с авторами - этап 1 | [Task](https://gitlab.com/miptfastapiproject/fastapi-project/-/issues/21) | [Merge request](https://gitlab.com/miptfastapiproject/fastapi-project/-/merge_requests/12) |
| Изменить структуру проекта | [Task](https://gitlab.com/miptfastapiproject/fastapi-project/-/issues/23) | [Merge request](https://gitlab.com/miptfastapiproject/fastapi-project/-/merge_requests/13) |
| Auth - этап 1 (разработать модели User, Role) | [Task](https://gitlab.com/miptfastapiproject/fastapi-project/-/issues/10) | [Merge request](https://gitlab.com/miptfastapiproject/fastapi-project/-/merge_requests/14) |
| Составить LLD - этап 1 (структура проекта) | [Task](https://gitlab.com/miptfastapiproject/fastapi-project/-/issues/24) | [Merge request](https://gitlab.com/miptfastapiproject/fastapi-project/-/merge_requests/17) |
| Разработать API для работы с авторами - этап 2 | [Task](https://gitlab.com/miptfastapiproject/fastapi-project/-/issues/25) | [Merge request](https://gitlab.com/miptfastapiproject/fastapi-project/-/merge_requests/19) |
| Разработать API для работы с жанрами | [Task](https://gitlab.com/miptfastapiproject/fastapi-project/-/issues/26) | [Merge request](https://gitlab.com/miptfastapiproject/fastapi-project/-/merge_requests/20) |
| Разработать API для работы с пользователями - этап 1 | [Task](https://gitlab.com/miptfastapiproject/fastapi-project/-/issues/27) | [Merge request](https://gitlab.com/miptfastapiproject/fastapi-project/-/merge_requests/21) |
| Разработать API для регистрации, авторизации и аутентификации | [Task](https://gitlab.com/miptfastapiproject/fastapi-project/-/issues/11) | [Merge request](https://gitlab.com/miptfastapiproject/fastapi-project/-/merge_requests/22) |
| Исправить работу exception handlers | [Task](https://gitlab.com/miptfastapiproject/fastapi-project/-/issues/29) | [Merge request](https://gitlab.com/miptfastapiproject/fastapi-project/-/merge_requests/23) |
| Разработать API для работы с авторами - этап 3 | [Task](https://gitlab.com/miptfastapiproject/fastapi-project/-/issues/22) | [Merge request](https://gitlab.com/miptfastapiproject/fastapi-project/-/merge_requests/31) |
| Личный кабинет пользователя для отслеживания прочитанных книг | [Task](https://gitlab.com/miptfastapiproject/fastapi-project/-/issues/16) | [Merge request](https://gitlab.com/miptfastapiproject/fastapi-project/-/merge_requests/33) |
| Тестирование - настроить тестовую среду | [Task](https://gitlab.com/miptfastapiproject/fastapi-project/-/issues/30) | [Merge request](https://gitlab.com/miptfastapiproject/fastapi-project/-/merge_requests/35) |
| Написать тесты на api Genre | [Task](https://gitlab.com/miptfastapiproject/fastapi-project/-/issues/32) | [Merge request](https://gitlab.com/miptfastapiproject/fastapi-project/-/merge_requests/37) |

**Использованные технологии и инструменты**

- Разработка: Python, FastAPI, Pydantic V2, SQLAlchemy
- БД, миграции: PostgreSQL, Alembic
- Обеспечение качества кода: Pytest, Pyright, Ruff
- Авторизация, безопасность: Baerer authorization, JWT, bcrypt
- Документация: OpenAPI/Swagger, Markdown
- Деплой: Docker, Docker Compose
- Командная разработка: Git/Gitlab

### Саморефлексия

**Достижения**

Данное приложение - первое мое приложение на фреймворке `FastAPI`, да и на ЯП `Python` в принципе. Поэтому выполнение этого задания для меня было крайне полезным. Я принял участие в создании всех основых частей приложения, разобрался как реализуются все концепции стандартного `CRUD`-приложения на данном стеке.

**Трудности**

Самой большой трудностью было разобраться с определением связей между сущностями (`one-to-one`, `one-to-many`/`many-to-one`, `many-to-many`). Если с тем когда какую из них использовать все +/- понятно, то с описанием этих связей с помощью инструментов `ORM SQLAlchemy` было много вопросов - какие дополнительные параметры для этих связей задавать (`onDelete`, `lazy`, `onCascade` и пр.)

Эти трудности возникли в следствии того, что писать полноценный проект, требующий проектирование БД и описание связей в ней мы начали до прохождения курса по БД. Это, конечно, недоработка в проектировании учебной программы.

### Общие впечатления от командной работы

В целом работа в команде соответствовала лучшим практикам профессиональной командной разработки. Задачи заводились и декомпозировались на доске задач, все члены команды принимали участие в обсуждении технических решений, оперативно реагировали на вопросы в чате команды.

Отдельно хочу отметить взаимодействие с тимлидом команды - Егором Калугиным (в силу своего опыта, он так же взял на себя роль техлида). У меня есть коммерческий опыт командной разработки и я могу с абсолютной уверенностью сказать, что Егор очень профессионально проводил ревью кода, давал комментарии и ссылки на источники/документацию. Его ревью не были придирками или формальностями - а как раз тем самым необходимым и важным звеном, от которого во многом зависит развитие начинающих специалистов и создание качественного, поддерживаемого, масштабируемого кода production-уровня. Посмотрите ссылки на MR - там видно как много существенных моментов он подсвечивает в ревью.

# Use the requested Python version
ARG PYTHON_VERSION=3.14-slim
FROM python:${PYTHON_VERSION}

# build args
ARG POETRY_VERSION=1.8.3
ENV POETRY_VERSION=${POETRY_VERSION}

# create app user
RUN useradd --create-home app
WORKDIR /app

# system deps for building some wheels and curl for installing node if needed
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential\
    && rm -rf /var/lib/apt/lists/*

# copy only poetry files first to leverage docker cache
COPY pyproject.toml poetry.lock* /app/

# install poetry in container python and configure to install into system env
RUN python -m pip install --upgrade pip \
    && python -m pip install "poetry==${POETRY_VERSION}" --no-cache-dir \
    && poetry config virtualenvs.create false --local


# export and install dependencies using poetry
ARG INSTALL_DEV=false
RUN if [ "$INSTALL_DEV" = "true" ]; then \
    poetry install --no-interaction --no-ansi --with dev; \
    else \
    poetry install --no-interaction --no-ansi --no-dev; \
    fi

# copy application code
COPY . /app

# Ensure files are owned by non-root user
RUN chown -R app:app /app
USER app

# Expose port and set environment defaults
ENV PYTHONUNBUFFERED=1
ENV PORT=8000
EXPOSE ${PORT}

CMD ["sh", "-c", "alembic upgrade head && python -m uvicorn src.main:app --host 0.0.0.0 --port ${PORT}"]

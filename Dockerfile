# Use the requested Python version
ARG PYTHON_VERSION=3.14-slim
FROM python:${PYTHON_VERSION}

# build args
ARG POETRY_VERSION=1.8.3
ENV POETRY_VERSION=${POETRY_VERSION}

# create app user
RUN useradd --create-home app
WORKDIR /app

# copy only poetry files first to leverage docker cache
COPY pyproject.toml poetry.lock* /app/

# install poetry in container python and configure to install into system env
RUN python -m pip install --upgrade pip \
    && python -m pip install "poetry==${POETRY_VERSION}" --no-cache-dir \
    && poetry config virtualenvs.create false --local

# export and install dependencies using poetry (no dev packages)
RUN poetry install --no-interaction --no-ansi --no-dev

# copy application code
COPY . /app

# Ensure files are owned by non-root user
RUN chown -R app:app /app
USER app

# Expose port and set environment defaults
ENV PYTHONUNBUFFERED=1
ENV PORT=8000
EXPOSE ${PORT}

CMD ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "${PORT}"]
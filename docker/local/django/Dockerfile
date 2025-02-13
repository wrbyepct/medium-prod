ARG PYTHON_VERSION=3.11.4-bullseye

FROM python:${PYTHON_VERSION} as python


FROM python as builder

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 


WORKDIR /app

COPY ["poetry.lock", "pyproject.toml", "README.md", "./"]

RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    libpq-dev \
    && pip install --upgrade pip \
    && pip install poetry==1.7.1 \
    && poetry install --no-root --no-ansi 


FROM python as runner
ARG APP_HOME=/app \
    VOLUME_DIR=/vol

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    IN_DOCKER=1 \
    DJANGO_DEBUG=1 \
    VIRTUAL_ENV="${APP_HOME}/.venv" \
    PATH="${APP_HOME}/.venv/bin:${PATH}"


WORKDIR $APP_HOME

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}


RUN apt-get update && apt-get install --no-install-recommends -y \
    libpq-dev \
    gettext  \
    && apt-get purge -y --auto-remove -o APT::AutoRemoveImportant=false \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


COPY local local
COPY core core 
COPY pyproject.toml pyproject.toml

COPY ["./docker/local/django/entrypoint", "./docker/local/django/start", "./docker/local/django/celery/worker/start_celeryworker", "./docker/local/django/celery/flower/start_flower", "/"]

RUN sed -i 's/\r$//g' /entrypoint /start /start_flower /start_celeryworker \
    && chmod +x /entrypoint /start /start_flower /start_celeryworker

RUN adduser \
    --disabled-password \
    --no-create-home \
    medium-api \
    && mkdir -p ${VOLUME_DIR}/api/staticfiles ${VOLUME_DIR}/api/mediafiles \
    && chown -R medium-api:medium-api $VOLUME_DIR $APP_HOME \
    && chmod -R 755 $VOLUME_DIR $APP_HOME

USER medium-api

ENTRYPOINT [ "/entrypoint" ]

ARG PYTHON_VERSION=3.11.4-slim-buster
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


FROM python AS runner
ARG APP_HOME=/app \
    VOLUME_DIR=/vol/api \
    UID=101

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    IN_DOCKER=1 \
    DJANGO_DEBUG=0 \
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


COPY core core 
COPY pyproject.toml pyproject.toml

COPY ["./docker/prod/django/start", "./docker/prod/django/celery/worker/start_celeryworker", "./docker/prod/django/celery/flower/start_flower", "/"]

RUN sed -i 's/\r$//g' /start /start_flower /start_celeryworker \
    && chmod +x /start /start_flower /start_celeryworker

RUN adduser \
    --uid $UID \
    --disabled-password \
    --no-create-home \
    medium-api \
    && mkdir -p ${VOLUME_DIR}/staticfiles ${VOLUME_DIR}/mediafiles \
    && chown -R medium-api:medium-api $VOLUME_DIR $APP_HOME \
    && chmod -R 755 $VOLUME_DIR $APP_HOME

USER medium-api

VOLUME $VOLUME_DIR/staticfiles
VOLUME $VOLUME_DIR/mediafiles

ENTRYPOINT [ "/start" ]

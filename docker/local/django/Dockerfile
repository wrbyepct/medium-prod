ARG PYTHON_VERSION=3.11.4-bullseye

FROM python:${PYTHON_VERSION} as python


FROM python as builder

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    libpq-dev

RUN pip install --upgrade pip && \
    pip install poetry==1.7.1

COPY ["poetry.lock", "pyproject.toml", "./"]
COPY README.md .

RUN poetry install --no-root --no-ansi && \
    rm -rf $POETRY_CACHE_DIR


FROM python as runner
ARG APP_HOME=/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

WORKDIR $APP_HOME

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

RUN apt-get update && apt-get install --no-install-recommends -y \
    libpq-dev \
    gettext  \
    && apt-get purge -y --auto-remove -o APT::AutoRemoveImportant=false \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY ./docker/local/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./docker/local/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY logs logs
COPY local local
COPY core core 

ENTRYPOINT [ "/entrypoint" ]
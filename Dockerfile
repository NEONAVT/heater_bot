FROM python:3.12-slim

WORKDIR /app
COPY pyproject.toml poetry.lock /app/

# Отключаем создание виртуального окружения
ENV POETRY_VIRTUALENVS_CREATE=false

RUN pip install --no-cache-dir poetry \
    && poetry install --no-root --no-interaction

COPY . /app

CMD ["python", "main.py"]
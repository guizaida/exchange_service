FROM python:3.9-slim

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/

RUN curl -sSL https://install.python-poetry.org | python3 -

RUN poetry config virtualenvs.create false

RUN poetry install --no-dev

COPY . /app

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

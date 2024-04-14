FROM python:3.9-slim

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/

RUN apt-get update && \
    apt-get install -y curl && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    apt-get remove -y curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV PATH="/root/.local/bin:${PATH}"

RUN poetry --version

RUN poetry config virtualenvs.create false

RUN poetry install --no-dev

COPY . /app

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

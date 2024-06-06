FROM python:3.12.3-slim-bookworm@sha256:afc139a0a640942491ec481ad8dda10f2c5b753f5c969393b12480155fe15a63

ENV POETRY_VERSION 1.8.3

RUN set -ex; pip install --no-cache-dir poetry==$POETRY_VERSION;

RUN apt-get update && apt-get install -y \
    curl \
    chromium-driver \
    && apt-get clean

WORKDIR /web-scrapper

COPY pyproject.toml poetry.lock /web-scrapper/

RUN poetry install --no-interaction --no-ansi

COPY . /web-scrapper

COPY .env /web-scrapper/

# Run the script inside the poetry shell
CMD ["poetry", "run", "python", "main.py"]

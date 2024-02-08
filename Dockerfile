FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1


RUN mkdir -p /usr/src
WORKDIR /usr/src

RUN apt update && \
    pip install --upgrade pip && \
    pip install poetry --no-cache-dir && \
    poetry config virtualenvs.create false

COPY . .

RUN poetry install

RUN chmod a+x docker_scripts/*.sh
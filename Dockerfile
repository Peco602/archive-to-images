FROM python:3.8-slim-buster

LABEL name="Archive-To-Images"
LABEL description="Archive-To-Images is a Python CLI to transform archives into images and reverse."
LABEL maintainer="Peco602 <giovanni1.pecoraro@protonmail.com>"

RUN mkdir /app /workspace

COPY . /app
WORKDIR /app

ENV PYTHONPATH=${PYTHONPATH}:${PWD} 

RUN pip3 install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

WORKDIR /workspace

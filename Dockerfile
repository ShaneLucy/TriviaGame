FROM python:3.9-rc-alpine

ENV PYTHONUBBUFFERED 1

COPY ./requirements.txt /requirements.txt

RUN apk update --no-cache 
RUN apk add --no-cache --virtual .tmp-build-deps \
        gcc postgresql-dev  \
        musl-dev python3-dev

RUN pip install -r /requirements.txt

RUN mkdir /Backend
WORKDIR /Backend
COPY ./Backend /Backend

RUN adduser -D user
USER user
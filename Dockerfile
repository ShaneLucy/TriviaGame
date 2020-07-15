FROM python:3.7-alpine

ENV PYTHONUBBUFFERED 1

COPY ./requirements.txt /requirements.txt

RUN apk update --no-cache 
RUN apk add --no-cache --virtual .tmp-build-deps \
        gcc postgresql-dev  \
        musl-dev python3-dev
RUN apk add build-base py-pip jpeg-dev zlib-dev
ENV LIBRARY_PATH=/lib:/usr/lib

RUN pip install -r /requirements.txt

RUN mkdir /Backend
WORKDIR /Backend
COPY ./Backend /Backend

RUN adduser -D user
USER user
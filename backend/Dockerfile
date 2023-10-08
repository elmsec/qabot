# pull official base image
FROM python:3.11.5-alpine

# set work directory
WORKDIR /usr/src/backend

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt .
COPY ./requirements-dev.txt .

RUN apk update
RUN apk add --virtual build-deps \
        # gcc \
        python3-dev musl-dev \
        libressl-dev libffi-dev
        # cargo \
# RUN apk add postgresql-dev
RUN pip install --upgrade pip
    # && apk add jpeg-dev zlib-dev libjpeg \
RUN pip install -r requirements-dev.txt
RUN apk del build-deps

RUN apk add curl

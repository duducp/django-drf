# pull official base image
FROM python:3.8

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements/base.txt .
COPY ./requirements/test.txt .
COPY ./requirements/dev.txt .
COPY ./requirements/prod.txt .
RUN pip install -r prod.txt

# copy project
COPY . .

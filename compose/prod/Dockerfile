FROM python:3.10.4-slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1 \
    PYTHONUNBUFFERED 1
ENV APP_HOME=/app

# install initial dependencies
RUN apt-get update && \
    apt-get -y install libpq-dev gcc gdal-bin &&  \
    pip install --no-cache --upgrade pip pipenv

WORKDIR ${APP_HOME}

# create the app user & permit to use app files
RUN addgroup appgroup && useradd -g appgroup appuser && \
    chown -R appuser:appgroup $APP_HOME

# install dependencies
COPY Pipfile Pipfile.lock ${APP_HOME}/
RUN pipenv requirements > ${APP_HOME}/requirements.txt && \
    pip install -r ${APP_HOME}/requirements.txt

COPY src/ ${APP_HOME}/src

# change to the app user
USER appuser

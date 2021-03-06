# HexOceanTask

## Overview

Hi! Requirements for this project are located at docs/requirements.md. I've used my own public template for building [DRF API](https://github.com/DiceNameIsMy/proper-DRF-startup); It includes Swagger documentation generator and celery(removed from this project). For dependency management system I use Pipenv because of its scripting capabilities. For authentication JWT tokens are used.

### I'd like to mention:

- I chose AWS S3 buckets for storing images because of it's scaleability, It has to be configured in .env files.
- I did not configure CI to this project, but I can(I have experience in building CI pipelines in GitLab)
- To be honest I think I'd better use FastAPI for this architecture. We have to send multiple requests while handling each HTTP request and FastAPI with it's builtin support for async views seems to be much better choice.

## Run project locally

1. Copy .env-sample file as .env in the same directory

    cp compose/local/.env-sample compose/local/.env

Optionally configure AWS S3 buckets in copied .env file

2. Build and run image via docker-compose:

    pipenv run compose --build

If you've set USE_AWS_S3_FOR_STATICFILES=True also run `docker-compose exec api ./src/manage.py collecstatic`. It might take 1-2 minutes to upload all staticfiles to S3 bucket

(There is an issue when api might start faster than db and raise an error becouse it couldn't connect to it. In this case just Ctrl+C and rerun the command)

3. Open http://localhost:8000/docs/swagger/ for an API overview

## Setup for development

    pipenv run setup

## Run tests(after setup)

    pipenv run test

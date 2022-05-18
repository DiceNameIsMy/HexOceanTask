# HexOceanTask


## Run project locally

Copy .env-sample file as .env in the same directory

    cp compose/local/.env-sample compose/local/.env

Build and run image via docker-compose:

    pipenv run compose --build

## Setup for development

    pipenv run setup

## Run tests(after setup)

    pipenv run compose -d pg
    cd src/
    pipenv run pytest
    docker kill $(docker ps -q)

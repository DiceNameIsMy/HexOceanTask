# proper-DRF-startup
My vision of proper(but not perfect yet) Django REST Framework application

## Run project locally

Copy .env-sample file as .env in the same directory

    cp compose/local/.env-sample compose/local/.env

Build and run image via docker-compose:

    pipenv run compose --build


## Setup for development

    pipenv run setup

## Run tests(after setup)

    cd src/
    pipenv run compose -d pg
    pipenv run pytest

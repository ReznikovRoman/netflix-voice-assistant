# Netflix Voice Assistant
Service for working with  _Netflix_ voice assistants.

## Stack
[FastAPI](https://fastapi.tiangolo.com/), [Yandex.Dialogs](https://yandex.ru/dev/dialogs/alice/doc/about.html)
(voice assistant provider)

## Services
- Netflix Admin:
  - Online-cinema management panel. Admins can manage films, genres, actors/directors/writers/...
  - https://github.com/ReznikovRoman/netflix-admin
- Netflix ETL:
  - ETL pipeline for synchronizing data between "Netflix Admin" database and Elasticsearch
  - https://github.com/ReznikovRoman/netflix-etl
- Netflix Movies API:
  - Movies API
  - https://github.com/ReznikovRoman/netflix-movies-api
    - Python client: https://github.com/ReznikovRoman/netflix-movies-client
- Netflix Auth API:
  - Authorization service - users and roles management
  - https://github.com/ReznikovRoman/netflix-auth-api
- Netflix UGC:
  - Service for working with user generated content (comments, likes, film reviews, etc.)
  - https://github.com/ReznikovRoman/netflix-ugc
- Netflix Notifications:
  - Notifications service (email, mobile, push)
  - https://github.com/ReznikovRoman/netflix-notifications
- Netflix Voice Assistant:
  - Online-cinema voice assistant
  - https://github.com/ReznikovRoman/netflix-voice-assistant

## Configuration
Docker containers:
 1. server
 2. traefik

docker-compose files:
 1. `docker-compose.yml` - for local development.
 2. `docker-compose-dev.yml` - for local development (without traefik).
 3. `tests/functional/docker-compose.yml` - for functional tests.

To run docker containers, you need to create a `.env` file in the root directory.

**`.env` example:**

```dotenv
ENV=.env

# Python
PYTHONUNBUFFERED=1

# Netflix Voice Assistant
# Project
NVA_DEBUG=1
NVA_PROJECT_BASE_URL=http://api-voice-assistant.localhost:8012
NVA_SERVER_PORT=8005
NVA_PROJECT_NAME=netflix-voice-assistant
NVA_API_V1_STR=/api/v1
NVA_SERVER_NAME=localhost
NVA_SERVER_HOSTS=http://api-voice-assistant.localhost:8012
# Netflix Movies
NVA_NETFLIX_MOVIES_BASE_URL=http://traefik:80
# Config
NVA_USE_STUBS=0
NVA_TESTING=0
NVA_CI=0
```

### Start project:

Locally:
```shell
docker-compose build
docker-compose up
```

## Development
Sync environment with `requirements.txt` / `requirements.dev.txt` (will install/update missing packages, remove redundant ones):
```shell
make sync-requirements
```

Compile requirements.\*.txt files (have to re-compile after changes in requirements.\*.in):
```shell
make compile-requirements
```

Use `requirements.local.in` for local dependencies; always specify _constraints files_ (-c ...)

Example:
```shell
# requirements.local.txt

-c requirements.txt

ipython
```

### Tests
Run unit tests (export environment variables from `.env` file):
```shell
export $(echo $(cat .env | sed 's/#.*//g'| xargs) | envsubst) && make test
```

To run functional tests, you need to create `.env` in ./tests/functional directory

**`.env` example:**
```dotenv
ENV=.env

# Python
PYTHONUNBUFFERED=1

# Netflix Voice Assistant
# Project
NVA_DEBUG=1
NVA_PROJECT_BASE_URL=http://api-voice-assistant.localhost:8012
NVA_SERVER_PORT=8005
NVA_PROJECT_NAME=netflix-voice-assistant
NVA_API_V1_STR=/api/v1
NVA_SERVER_NAME=localhost
NVA_SERVER_HOSTS=http://api-voice-assistant.localhost:8012
# Netflix Movies
NVA_NETFLIX_MOVIES_BASE_URL=http://traefik:80
# Config
NN_USE_STUBS=1
NN_TESTING=1
NN_CI=0
```

Run functional tests:
```shell
cd ./tests/functional && docker-compose up test
```

Makefile recipe:
```shell
make dtf
```

### Code style:
Before pushing a commit run all linters:

```shell
make lint
```

### pre-commit:
pre-commit installation:
```shell
pre-commit install
```

## Documentation
OpenAPI 3 documentation:
- `${PROJECT_BASE_URL}/api/v1/docs` - Swagger

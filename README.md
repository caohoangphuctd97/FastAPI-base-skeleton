# SaanSook API

## Getting Started

This is SaanSook API

## Folder Structure

```Bash
.
├── assets # Contains all assets, like service account keys
│   ├── key # These keys will be ignored by git
│   │   └── key_dev.json
│   │   └── key_prod.json
├── environments # Contains environment variables for the function
│   └── dev
├── migrations # Migrations databse version
├── app # Main logic code
│   ├── auth # Declare Auth Credentials for app
│   ├── apis # The views layer
│   │   ├── __init__.py
│   │   ├── custom_types.py # Custom paging header for response
│   │   ├── health.py # The health endpoint
│   │   ├── customers.py # The customers endpoint
│   │   ├── devices.py # The devices endpoint
│   ├── controllers # The controllers layer
│   │   ├── __init__.py
│   │   ├── helpers.py # Helper functions used for controllers
│   │   ├── custom_types.py # Custom some error handler for controllers
│   │   ├── customers.py # The customers controller
│   │   ├── devices.py # The devices controller
│   ├── database # The models layer
│   │   ├── __init__.py
│   │   ├── config.py # Config naming convention for database
│   │   ├── depends.py # Add dependency for database
│   │   └── models.py # Declare models
│   ├── __init__.py
│   ├── _version.py
│   ├── config.py # Config for main app (paging, auth0, database, datadog variables)
│   ├── configure_logging.py # Config for logging
│   ├── main.py # Init app, declare route health, swagger
│   ├── middlewares.py # Add middlewares for app (tracing, proxy header, cors)
│   ├── schemas.py # Schemas for response models
│   └── utils.py # Utility for app
├── deploy
│   ├── charts # Helm charts
│   ├── developments # Env DEV deploy
│   ├── production # Env PRODUCTION deploy
│   └── qa # Env QA deploy
├── Makefile # Ignored by git
├── README.md
├── requirements.in
├── requirements.txt
├── tools # Contain all tools
└── tests # Contains all tests
    ├── integration_tests
    └── unit_tests
```

## Prerequisite

1. Linux (Ubuntu/Debian)
2. Python 3.8 and its tools installed
3. Install virtualenv and pip-compile

## Run app locally
```shell
# Follow instructions in [Set up PostgreSQL test database](#set-up-postgresql-test-database)
# to set up test database

# Set up virtual environment
virtualenv -p python3 venv

# Uncomment `create_database` startup hook in `app/main.py` to create tables
# if necessary. Remember to change it back after testing.

# Run app
export DATABASE_URI='postgresql://postgres:postgres@127.0.0.1:5432/saansook'
source venv/bin/activate
uvicorn --reload app.main:app
```

## Run unit tests locally

### Install PostgreSQL

```shell
# Create the file repository configuration:
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'

# Import the repository signing key:
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -

# Update the package lists:
sudo apt-get update

# Install the specific version of PostgreSQL used in production.
sudo apt-get -y install postgresql-13
```

### Set up PostgreSQL test database

```shell
# Change password for the default user `postgres`
sudo -u postgres psql
\password postgres
# Quit
\q

# Start the default PostgreSQL database cluster
sudo pg_ctlcluster 13 main start

# Create test database
sudo -u postgres createdb saansook

# Stop the database cluster after testing done
sudo pg_ctlcluster 13 main stop
```

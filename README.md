# Extract, Transform, Load (ETL)

This repository provides an ETL pipeline that integrates R-based data generation with a PostgreSQL database. .rds files produced by R scripts are served through a Plumber API and ingested into the database by a Python backend. The application uses Django to manage database models, migrations, and data ingestion workflows. This enables a seamless pipeline for end users to generate a reproducible database, while the Python integration lays the groundwork for future exploratory data analysis and machine learning workflows using Python libraries.

## Overview

- **R scripts** generate `.rds` data outputs
- **Plumber** exposes these outputs via RESTful API endpoints
- **Django** manages ORM-based schema creation and programmatically populates the database from external API sources.


## Setup Instructions

The user is responsible for creating the PostgreSQL database manually. Connection credentials should be configured in the .env file, which is loaded by settings.py.

### 1. Configure Database Settings

Update your `.env` file located at `backend/.env` with the following values:

```env
DATABASE_NAME=''
DATABASE_USER=''
DATABASE_PASSWORD=''
HOST=''
PORT=''
```
## Set Up and Populate the Database

After configuring your environment variables in `.env` and creating the PostgreSQL database, follow these steps:

### 1. Apply Migrations

Navigate to egrid-main directory and run:
```
Rscript run_api.R
```

Navigate to backend directory. Run the following commands to set up the database schema:

```bash
python manage.py makemigrations
python manage.py migrate
```
### 2. Populate the Database
Load data from the Plumber API by running:

```
python manage.py populate_egrid_db

```

 
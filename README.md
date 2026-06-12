# EventSphere API

Industry-level Event Management System built with FastAPI, PostgreSQL, SQLAlchemy and JWT Authentication.

## Features

* User Registration & Login
* JWT Authentication
* Role-Based Access Control (RBAC)
* Event Creation
* Event Update & Delete
* Event Registration
* Duplicate Registration Prevention
* My Events
* My Registrations
* Event Participants
* Search Events
* Pagination
* Admin Panel
* PostgreSQL Database
* Async SQLAlchemy

## Tech Stack

* FastAPI
* PostgreSQL
* SQLAlchemy
* Alembic
* Pydantic
* JWT Authentication
* Python 3.12

## Project Structure

```text
app/
├── api/
├── core/
├── models/
├── schemas/
├── services/
├── dependencies/
├── middleware/
└── utils/
```

## Installation

```bash
git clone https://github.com/PrinceSharmaBackend/EventSphere-API.git

cd EventSphere-API

python -m venv venv

source venv/bin/activate

pip install -r requirements.txt
```

## Run Application

```bash
uvicorn app.main:app --reload
```

## API Documentation

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

## Author

Prince Sharma

Backend Developer | FastAPI | PostgreSQL | Python

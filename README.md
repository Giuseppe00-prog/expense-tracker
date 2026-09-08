# Expense Tracker

A Python expense tracking application with a command-line interface and REST API, SQLite persistence, input validation and automated tests.

The project was developed incrementally, starting from a simple CLI application and evolving into a layered backend application with persistent storage and a REST API built with FastAPI.

## Features

* Add new expenses
* Display all recorded expenses
* Retrieve a single expense by ID
* Update existing expenses
* Remove expenses
* Calculate the total amount of recorded expenses
* Persist expenses in a SQLite database
* Validate expense data at both domain and API level
* REST API with full CRUD operations
* Automatic API documentation with FastAPI
* HTTP error handling with appropriate status codes
* Automated tests with pytest
* Isolated database and API tests using temporary SQLite databases

## Technologies

* Python
* FastAPI
* Pydantic
* SQLite
* Dataclasses
* Decimal
* pytest
* HTTPX / FastAPI TestClient
* Uvicorn
* Git & GitHub

## Project Structure

```text
expense-tracker/
├── api.py
├── database.py
├── gestione_spese.py
├── main.py
├── spesa.py
├── requirements.txt
├── tests/
│   ├── test_api.py
│   ├── test_database.py
│   └── test_gestione_spese.py
├── .gitignore
└── README.md
```

### Main Modules

* `spesa.py` — Defines the `Spesa` domain model and its validation rules.
* `database.py` — Handles SQLite database creation and CRUD operations.
* `gestione_spese.py` — Contains the application logic and coordinates domain objects with database operations.
* `main.py` — Provides the command-line interface.
* `api.py` — Exposes the application through a REST API built with FastAPI.
* `tests/` — Contains automated tests for database operations, application logic and REST API endpoints.

The SQLite database file (`spese.db`) is generated locally and excluded from version control.

## REST API

The application exposes the following endpoints:

| Method   | Endpoint      | Description                |
| -------- | ------------- | -------------------------- |
| `GET`    | `/`           | API information            |
| `GET`    | `/spese`      | Retrieve all expenses      |
| `GET`    | `/spese/{id}` | Retrieve an expense by ID  |
| `POST`   | `/spese`      | Create a new expense       |
| `PUT`    | `/spese/{id}` | Update an existing expense |
| `DELETE` | `/spese/{id}` | Delete an expense          |

Invalid input is validated through Pydantic and appropriate HTTP status codes such as `404` and `422` are returned when necessary.

## Installation

Clone the repository:

```bash
git clone https://github.com/Giuseppe00-prog/expense-tracker.git
cd expense-tracker
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Running the CLI

Run:

```bash
python main.py
```

The SQLite database is created automatically when needed.

## Running the REST API

Start the FastAPI development server:

```bash
uvicorn api:app --reload
```

The API will then be available locally.

FastAPI automatically provides interactive API documentation at:

```text
/docs
```

## Running Tests

Run the complete test suite with:

```bash
pytest
```

Tests use temporary SQLite databases where necessary, preventing the application's local database from being modified.

The test suite covers domain validation, database CRUD operations, application logic, API endpoints, HTTP errors and input validation.

## Architecture

The application separates its responsibilities into different layers:

```text
CLI / REST API
      ↓
Application logic
      ↓
Domain model
      ↓
Database layer
      ↓
SQLite
```

This structure keeps user interaction, business logic and data persistence separated and makes the application easier to test and evolve.

## Roadmap

Future improvements include:

* PostgreSQL persistence
* Improved SQL and database modelling
* Expense dates
* Filtering and searching expenses
* Monthly summaries
* React + TypeScript frontend
* Docker containerization
* Cloud deployment
* AI-powered features

# Expense Tracker

A Python expense tracking application with a command-line interface and REST API, PostgreSQL persistence, SQLAlchemy ORM, input validation and automated tests.

The project was developed incrementally, starting from a simple CLI application and evolving into a layered backend application with persistent storage, relational data modelling and a REST API built with FastAPI.

## Features

* Add new expenses
* Display all recorded expenses
* Retrieve a single expense by ID
* Update existing expenses
* Remove expenses
* Manage expense categories
* Persist expenses and categories in PostgreSQL
* Relational modelling between expenses and categories
* Validate expense data at both domain and API level
* REST API with full expense CRUD operations
* Automatic API documentation with FastAPI
* HTTP error handling with appropriate status codes
* Automated tests with pytest
* Isolated PostgreSQL database for testing

## Technologies

* Python
* FastAPI
* Pydantic
* PostgreSQL
* SQLAlchemy ORM
* Psycopg
* python-dotenv
* Decimal
* pytest
* HTTPX / FastAPI TestClient
* Uvicorn
* Git & GitHub

## Project Structure

```text
expense-tracker/
├── models/
│   ├── __init__.py
│   ├── base.py
│   ├── categoria.py
│   └── spesa.py
├── services/
│   ├── __init__.py
│   ├── gestione_categorie.py
│   └── gestione_spese.py
├── tests/
│   ├── conftest.py
│   ├── test_api.py
│   ├── test_database.py
│   ├── test_gestione_categorie.py
│   └── test_gestione_spese.py
├── api.py
├── database.py
├── main.py
├── pytest.ini
├── requirements.txt
├── .gitignore
└── README.md
```

### Main Modules

* `models/base.py` — Defines the SQLAlchemy declarative base used by the ORM models.
* `models/categoria.py` — Defines the `Categoria` ORM model and its validation rules.
* `models/spesa.py` — Defines the `Spesa` ORM model, validation rules and relationship with categories.
* `database.py` — Configures the SQLAlchemy engine and sessions and provides database CRUD operations.
* `services/gestione_categorie.py` — Contains application logic for category management.
* `services/gestione_spese.py` — Contains application logic for expense management.
* `main.py` — Provides the command-line interface.
* `api.py` — Exposes the application through a REST API built with FastAPI.
* `tests/` — Contains automated tests for persistence, application logic and REST API endpoints.

Database credentials and configuration are loaded from environment variables and are not stored in version control.

## Database Model

The application uses PostgreSQL with two related entities:

```text
Categorie
├── id
└── nome
      │
      │ 1:N
      ↓
Spese
├── id
├── descrizione
├── importo
└── categoria_id
```

Each expense belongs to one category, while a category can be associated with multiple expenses.

SQLAlchemy ORM maps the Python models to the PostgreSQL tables and manages persistence and relationships.

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

## Database Configuration

The application requires a PostgreSQL database.

Create a `.env` file in the project root with your local database configuration:

```text
DB_HOST=localhost
DB_PORT=5432
DB_NAME=expense_tracker
DB_USER=postgres
DB_PASSWORD=your_password
```

The `.env` file is excluded from version control.

The database schema currently includes the `categorie` and `spese` tables with a foreign key relationship between them.

## Running the CLI

Run:

```bash
python main.py
```

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

The project uses a separate PostgreSQL database for automated tests, keeping test data isolated from the development database.

Run the complete test suite with:

```bash
pytest
```

The test suite covers model validation, database CRUD operations, application logic, relational behaviour, API endpoints, HTTP errors and input validation.

## Architecture

The application separates its responsibilities into different layers:

```text
CLI / REST API
      ↓
Service layer
      ↓
SQLAlchemy ORM models
      ↓
Database layer / SQLAlchemy Session
      ↓
PostgreSQL
```

This structure keeps user interaction, business logic and persistence concerns separated, making the application easier to test, maintain and extend.

## Project Evolution

The project has been developed incrementally to explore progressively more advanced backend concepts:

```text
Python CLI
    ↓
Persistent storage
    ↓
Automated testing
    ↓
FastAPI REST API
    ↓
PostgreSQL
    ↓
Relational database modelling
    ↓
SQLAlchemy ORM
```

## Roadmap

Planned improvements include:

* Expense dates
* Filtering and searching expenses
* Monthly summaries and statistics
* React + TypeScript frontend
* Docker containerization
* Cloud deployment

AI-powered features may be explored in a future project or later evolution of the application.

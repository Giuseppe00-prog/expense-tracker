# Expense Tracker

A Python CLI application for tracking personal expenses, with SQLite persistence and automated tests.

## Features

* Add a new expense
* Display all recorded expenses
* Display the total amount of expenses
* Remove an expense
* Persist expenses in a SQLite database
* Load expenses from the database
* Validate expense data and user input
* Automated tests with pytest
* Isolated database tests using temporary databases

## Technologies

* Python
* SQLite
* Dataclasses
* Decimal
* pytest
* Git & GitHub

## Project Structure

```text
expense-tracker/
├── main.py
├── spesa.py
├── gestione_spese.py
├── database.py
├── test_gestione_spese.py
├── .gitignore
└── README.md
```

### Main Modules

* **`main.py`** — Handles the command-line interface and user interaction.
* **`spesa.py`** — Defines the `Spesa` data model and its validation rules.
* **`gestione_spese.py`** — Contains the main operations for adding and removing expenses, coordinating the application logic with the database.
* **`database.py`** — Handles SQLite database creation and CRUD operations for expenses.
* **`test_gestione_spese.py`** — Contains the automated tests for the application, including validation, application logic and database operations.

The SQLite database file (`spese.db`) is generated locally when the application is used and is excluded from version control through `.gitignore`.

## How to Run

Clone the repository and move into the project directory:

```bash
git clone <repository-url>
cd expense-tracker
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts\activate
```

Install the test dependency:

```bash
pip install pytest
```

Run the application:

```bash
python main.py
```

The SQLite database will be created locally when needed.

## Running Tests

To run the complete automated test suite:

```bash
pytest
```

The tests use temporary SQLite databases where necessary, so they do not modify the application's local database.

## Testing

The test suite covers:

* Expense creation
* Expense validation
* Adding expenses
* Removing expenses
* Handling non-existent expense IDs
* Total calculation
* SQLite database creation
* Inserting expenses into the database
* Reading expenses from the database
* Deleting expenses from the database
* CLI input handling
* Error handling
* Mocking user input and application dependencies

## Roadmap

Possible future improvements include:

* Filter expenses by category
* Search expenses
* Edit existing expenses
* Add dates to expenses
* Monthly expense summaries
* Improved CLI interface
* REST API
* Additional test coverage

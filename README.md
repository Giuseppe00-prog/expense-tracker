# Expense Tracker

A Python CLI application for tracking personal expenses, with JSON persistence and automated tests.

## Features

* Add a new expense
* Display all recorded expenses
* Display the total amount of expenses
* Remove an expense
* Save expenses to a JSON file
* Load expenses from a JSON file
* Validate expense data and user input
* Automated tests with pytest

## Technologies

* Python
* Dataclasses
* Decimal
* JSON
* pytest
* Git & GitHub

## Project Structure

```text
expense-tracker/
├── main.py
├── spesa.py
├── gestione_spese.py
├── test_gestione_spese.py
├── spese.json
├── .gitignore
└── README.md
```

### Main modules

* **`main.py`** — Handles the command-line interface and user interaction.
* **`spesa.py`** — Defines the `Spesa` data model and its validation rules.
* **`gestione_spese.py`** — Contains the main operations for adding, removing, saving and loading expenses.
* **`test_gestione_spese.py`** — Contains the automated tests for the application.
* **`spese.json`** — Stores the expenses locally.

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

## Running Tests

To run the automated test suite:

```bash
pytest
```

## Roadmap

Future improvements may include:

* Filter expenses by category
* Search expenses
* Edit existing expenses
* Add dates to expenses
* Monthly expense summaries
* Improved CLI interface
* Database persistence
* REST API
* Additional test coverage

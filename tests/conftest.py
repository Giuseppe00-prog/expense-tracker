import psycopg
import pytest
import database

@pytest.fixture
def database_test(monkeypatch):
    def get_connessione_test():
        return psycopg.connect(
            host="localhost",
            port=5432,
            dbname="expense_tracker_test",
            user="postgres",
            password=database.os.getenv("DB_PASSWORD")
        )

    monkeypatch.setattr(
        database,
        "get_connessione",
        get_connessione_test
    )

    with get_connessione_test() as connessione:
        with connessione.cursor() as cursore:
            cursore.execute("DELETE FROM spese")
            cursore.execute("DELETE FROM categorie")

    yield
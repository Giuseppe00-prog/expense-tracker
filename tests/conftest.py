import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

import database

@pytest.fixture
def database_test(monkeypatch):
    database_url_test = (
            f"postgresql+psycopg://"
            f"postgres:"
            f"{database.os.getenv('DB_PASSWORD')}@"
            f"localhost:5432/"
            f"expense_tracker_test"
        )

    engine_test = create_engine(database_url_test)

    SessionTest = sessionmaker(bind=engine_test, expire_on_commit=False)

    monkeypatch.setattr(
        database,
        "SessionLocal",
        SessionTest
    )

    with SessionTest() as session:
        session.execute(text("DELETE FROM spese"))
        session.execute(text("DELETE FROM categorie"))
        session.commit()

    yield

    engine_test.dispose()
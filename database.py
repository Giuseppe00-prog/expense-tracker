import os
from dotenv import load_dotenv
from models.categoria import Categoria
from models.spesa import Spesa
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, selectinload

load_dotenv()

DATABASE_URL = (
    f"postgresql+psycopg://"
    f"{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_NAME')}"
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

#OPERAZIONI CATEGORIA

def inserisci_categoria(categoria):
    with SessionLocal() as session:
        session.add(categoria)
        session.commit()
        session.refresh(categoria)

        return categoria.id

def aggiorna_categoria(categoria):
    with SessionLocal() as session:
        categoria_db = session.get(Categoria, categoria.id)

        if categoria_db is None:
            return False

        categoria_db.nome = categoria.nome

        session.commit()

        return True

def recupera_categoria_per_id(id_categoria):
    with SessionLocal() as session:
        return session.get(Categoria, id_categoria)

def recupera_categoria_per_nome(nome_categoria):
    with SessionLocal() as session:
        stmt = select(Categoria).where(
            Categoria.nome == nome_categoria
        )
        return session.scalar(stmt)

def leggi_categorie():
    with SessionLocal() as session:
        stmt = select(Categoria)

        return list(session.scalars(stmt))

def rimuovi_categoria(id_categoria):
    with SessionLocal() as session:
        categoria_db = session.get(Categoria, id_categoria)

        if categoria_db is None:
            return False

        session.delete(categoria_db)
        session.commit()

        return True

#OPERAZIONI SPESA
def inserisci_spesa(spesa):
    with SessionLocal() as session:
        categoria_db = session.get(Categoria, spesa.categoria.id)

        spesa.categoria = categoria_db

        session.add(spesa)
        session.commit()

        return spesa.id

def recupera_singola_spesa(id_spesa):
    with SessionLocal() as session:
        return session.get(Spesa, id_spesa, options=[selectinload(Spesa.categoria)])

def leggi_spese():
    with SessionLocal() as session:
        stmt = select(Spesa).options(
            selectinload(Spesa.categoria)
        )
        return list(session.scalars(stmt))

def rimuovi_spesa(id_spesa):
    with SessionLocal() as session:
        spesa = session.get(Spesa, id_spesa)

        if spesa is None:
            return False

        session.delete(spesa)
        session.commit()

        return True

def aggiorna_spesa(spesa):
    with SessionLocal() as session:
        spesa_db = session.get(Spesa, spesa.id)

        if spesa_db is None:
            return False

        categoria_db = session.get(Categoria, spesa.categoria.id)

        spesa_db.descrizione = spesa.descrizione
        spesa_db.importo = spesa.importo
        spesa_db.categoria = categoria_db

        session.commit()

        return True
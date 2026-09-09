import sqlite3
import os
import psycopg
from dotenv import load_dotenv

from decimal import Decimal

from models.categoria import Categoria
from models.spesa import Spesa

load_dotenv()

def get_connessione():
    return psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

#OPERAZIONI CATEGORIA

def inserisci_categoria(categoria):
    with get_connessione() as connessione:
        with connessione.cursor() as cursore:
            cursore.execute("INSERT INTO categorie (nome) VALUES (%s) RETURNING id;", (categoria.nome,))

            risultato = cursore.fetchone()
            return risultato[0]

def aggiorna_categoria(categoria):
    with get_connessione() as connessione:
        with connessione.cursor() as cursore:
            cursore.execute("UPDATE categorie SET nome = %s WHERE id = %s", (categoria.nome, categoria.id))

            return cursore.rowcount > 0

def recupera_categoria_per_id(id_categoria):
    with get_connessione() as connessione:
        with connessione.cursor() as cursore:
            cursore.execute("SELECT * FROM categorie WHERE id = %s", (id_categoria,))
            risultato = cursore.fetchone()
            if risultato is None:
                return None

            return Categoria(
                nome=risultato[1],
                id=risultato[0]
            )

def recupera_categoria_per_nome(nome_categoria):
    with get_connessione() as connessione:
        with connessione.cursor() as cursore:
            cursore.execute("SELECT * FROM categorie WHERE nome = %s", (nome_categoria,))
            risultato = cursore.fetchone()
            if risultato is None:
                return None

            return Categoria(
                nome=risultato[1],
                id=risultato[0]
            )

def leggi_categorie():
    with get_connessione() as connessione:
        with connessione.cursor() as cursore:
            cursore.execute("SELECT * FROM categorie")
            risultato = cursore.fetchall()

            lista_categorie = []
            for res in risultato:
                lista_categorie.append(Categoria(nome=res[1], id=res[0]))

            return lista_categorie

def rimuovi_categoria(id_categoria):
    with get_connessione() as connessione:
        with connessione.cursor() as cursore:
            cursore.execute("DELETE FROM categorie WHERE id = %s", (id_categoria,))

            return cursore.rowcount > 0

#OPERAZIONI SPESA
def inserisci_spesa(spesa):
    with get_connessione() as connessione:
        with connessione.cursor() as cursore:
            cursore.execute("INSERT INTO spese (descrizione, importo, categoria_id) VALUES (%s, %s, %s) RETURNING id", (spesa.descrizione, spesa.importo, spesa.categoria.id))

            risultato = cursore.fetchone()

            return risultato[0]

def recupera_singola_spesa(id_spesa):
    with get_connessione() as connessione:
        with connessione.cursor() as cursore:
            cursore.execute(
                """
                SELECT
                    s.id,
                    s.descrizione,
                    s.importo,
                    c.id,
                    c.nome
                FROM spese AS s 
                JOIN categorie AS c ON c.id = s.categoria_id
                WHERE s.id = %s
                """,
                (id_spesa,)
                            )

            risultato = cursore.fetchone()

            if risultato is None:
                return None

            categoria = Categoria(
                id = risultato[3],
                nome = risultato[4]
            )
            return Spesa(
                descrizione=risultato[1],
                categoria = categoria,
                importo=risultato[2],
                id=risultato[0]
            )

def leggi_spese():
    with get_connessione() as connessione:
        with connessione.cursor() as cursore:
            cursore.execute(
                """
                SELECT
                    s.id,
                    s.descrizione,
                    s.importo,
                    c.id,
                    c.nome
                FROM spese AS s
                JOIN categorie AS c
                    ON s.categoria_id = c.id
                """
            )

            risultati = cursore.fetchall()

            lista_spese = []

            for risultato in risultati:
                categoria = Categoria(
                    id=risultato[3],
                    nome=risultato[4]
                )

                spesa = Spesa(
                    descrizione=risultato[1],
                    categoria=categoria,
                    importo=risultato[2],
                    id=risultato[0]
                )

                lista_spese.append(spesa)

            return lista_spese

def rimuovi_spesa(id_spesa):
    with get_connessione() as connessione:
        with connessione.cursor() as cursore:
            cursore.execute("DELETE FROM spese WHERE id = %s", (id_spesa,))

            return cursore.rowcount > 0

def aggiorna_spesa(spesa):
    with get_connessione() as connessione:
        with connessione.cursor() as cursore:
            cursore.execute(
                """
                UPDATE spese
                SET
                    descrizione = %s,
                    importo = %s,
                    categoria_id = %s
                WHERE id = %s
                """,
                (
                    spesa.descrizione,
                    spesa.importo,
                    spesa.categoria.id,
                    spesa.id
                )
            )

            return cursore.rowcount > 0
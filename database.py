import sqlite3
from decimal import Decimal

from spesa import Spesa


def crea_database(percorso_spesa="spese.db"):
    """Crea il database e la tabella spese se non esistono"""
    with sqlite3.connect(percorso_spesa) as connessione:
        connessione.execute(
            """
            CREATE TABLE IF NOT EXISTS spese (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                descrizione TEXT NOT NULL,
                categoria TEXT NOT NULL,
                importo REAL NOT NULL
            )
            """
        )


def inserisci_spesa(spesa, percorso_spesa="spese.db"):
    """Inserisce una nuova spesa nel database e restituisce l'id generato."""
    with sqlite3.connect(percorso_spesa) as connessione:
        istruzione_sql = """
            INSERT INTO spese (descrizione, categoria, importo) VALUES (?, ?, ?)
        """
        # SQLite salva l'importo come REAL, quindi convertiamo Decimal in float prima dell'inserimento.
        risultato = connessione.execute(istruzione_sql, [spesa.descrizione, spesa.categoria, float(spesa.importo)])

        id_generato = risultato.lastrowid

        return id_generato


def leggi_spese(percorso_spesa ="spese.db"):
    """Recupera tutte le spese dal database."""
    with sqlite3.connect(percorso_spesa) as connessione:
        risultato = connessione.execute("SELECT * FROM spese")

        lista_spese = []

        # Convertiamo il valore letto da SQLite in Decimal per mantenere la gestione precisa degli importi nell'applicazione.
        for riga in risultato:
            spesa = Spesa(
                descrizione=riga[1],
                categoria=riga[2],
                importo=Decimal(str(riga[3])),
                id= riga[0]
            )
            lista_spese.append(spesa)

        return lista_spese

def rimuovi_spesa(id_spesa, percorso_spesa="spese.db"):
    """Rimuove dal database la spesa identificata dall'id."""
    with sqlite3.connect(percorso_spesa) as connessione:
        istruzione_sql = """
            DELETE FROM spese
            WHERE id = ?
        """

        connessione.execute(istruzione_sql, [id_spesa])


if __name__ == "__main__":
    crea_database()
    print(leggi_spese())
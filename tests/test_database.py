import sqlite3
from decimal import Decimal

import pytest

import gestione_spese
from database import crea_database, inserisci_spesa, leggi_spese, recupera_singola_spesa, aggiorna_spesa
from spesa import Spesa

@pytest.fixture
def lista_spese():
    return [
        Spesa("Spesa 1", "Casa", Decimal("10.00"), 1),
        Spesa("Spesa 2", "Cibo", Decimal("20.00"), 2),
        Spesa("Spesa 3", "Svago", Decimal("15.00"), 3),
    ]

def test_crea_database(tmp_path):
    percorso_db_tmp = tmp_path / "spese.db"

    crea_database(percorso_db_tmp)

    with sqlite3.connect(percorso_db_tmp) as connessione:
        risultato = connessione.execute('SELECT name FROM sqlite_master WHERE type = "table"')
        tabelle = risultato.fetchall()
        esiste_tabella_spese = any(t[0] == 'spese' for t in tabelle)
        assert  esiste_tabella_spese

def test_inserisci_spesa(tmp_path):
    percorso_db_tmp = tmp_path / "spese.db"

    crea_database(percorso_db_tmp)

    spesa = Spesa("Pizza", "Cibo", Decimal("12.50"))

    id_generato = inserisci_spesa(spesa, percorso_db_tmp)

    assert id_generato is not None
    assert isinstance(id_generato, int)

    with sqlite3.connect(percorso_db_tmp) as connessione:
        risultato = connessione.execute('SELECT * from spese')
        riga = risultato.fetchone()
        assert riga[0] == id_generato
        assert riga[1] == spesa.descrizione
        assert riga[2] == spesa.categoria
        assert Decimal(str(riga[3])) == spesa.importo

def test_leggi_spese(tmp_path):
    percorso_db_tmp = tmp_path / "spese.db"

    crea_database(percorso_db_tmp)

    spesa1 = Spesa("Pizza", "Cibo", Decimal("12.50"))
    spesa2 = Spesa("Cinema", "Svago", Decimal("8.00"))

    id1 = inserisci_spesa(spesa1, percorso_db_tmp)
    id2 = inserisci_spesa(spesa2, percorso_db_tmp)

    spese = leggi_spese(percorso_db_tmp)

    assert len(spese) == 2

    assert spese[0].id == id1
    assert spese[0].descrizione == spesa1.descrizione
    assert spese[0].categoria == spesa1.categoria
    assert spese[0].importo == spesa1.importo

    assert spese[1].id == id2
    assert spese[1].descrizione == spesa2.descrizione
    assert spese[1].categoria == spesa2.categoria
    assert spese[1].importo == spesa2.importo

def test_rimuovi_spesa(lista_spese, tmp_path):

    percorso_db_tmp = tmp_path / "spese.db"

    crea_database(percorso_db_tmp)

    for spesa in lista_spese:
        inserisci_spesa(spesa, percorso_db_tmp)

    spesa_rimossa = gestione_spese.rimuovi_spesa(2, percorso_db_tmp)

    spese_db = leggi_spese(percorso_db_tmp)


    spesa_ancora_presente = False
    for spesa in spese_db:
        if spesa.id == 2:
            spesa_ancora_presente = True
            break

    assert spesa_rimossa is True
    assert spesa_ancora_presente is False

def test_rimuovi_spesa_id_non_esistente(lista_spese, tmp_path):
    percorso_db_tmp = tmp_path / "spese.db"

    crea_database(percorso_db_tmp)

    for spesa in lista_spese:
        inserisci_spesa(spesa, percorso_db_tmp)

    spesa_rimossa = gestione_spese.rimuovi_spesa(99, percorso_db_tmp)

    spese_db = leggi_spese(percorso_db_tmp)

    assert spesa_rimossa is False
    assert len(spese_db) == len(lista_spese)

def test_recupera_singola_spesa(tmp_path):
    percorso_db_tmp = tmp_path / "spese.db"
    crea_database(percorso_db_tmp)


    spesa1 = Spesa("Pizza", "Cibo", Decimal("12.50"))
    spesa2 = Spesa("Cinema", "Svago", Decimal("8.00"))

    id1 = inserisci_spesa(spesa1, percorso_db_tmp)
    id2 = inserisci_spesa(spesa2, percorso_db_tmp)

    spesa_recuperata = recupera_singola_spesa(id1, percorso_db_tmp)

    assert spesa_recuperata.id == id1
    assert spesa_recuperata.descrizione == spesa1.descrizione
    assert spesa_recuperata.categoria == spesa1.categoria
    assert spesa_recuperata.importo == spesa1.importo

def test_recupera_singola_spesa_id_non_esistente(tmp_path):
    percorso_db_tmp = tmp_path / "spese.db"
    crea_database(percorso_db_tmp)
    spesa_recuperata = recupera_singola_spesa(10, percorso_db_tmp)

    assert spesa_recuperata is None

def test_aggiorna_spesa(tmp_path):
    percorso_db_tmp = tmp_path / "spese.db"
    crea_database(percorso_db_tmp)
    spesa_originale = Spesa(
        "Pizza",
        "Cibo",
        Decimal("12.50")
    )
    id_spesa = inserisci_spesa(spesa_originale, percorso_db_tmp)
    spesa_aggiornata = Spesa(
        "Benzina",
        "Auto",
        Decimal("50.00"),
        id_spesa
    )
    risultato = aggiorna_spesa(id_spesa, spesa_aggiornata, percorso_db_tmp)

    assert risultato is True

    spesa_recuperata = recupera_singola_spesa(id_spesa, percorso_db_tmp)

    assert spesa_recuperata == spesa_aggiornata

def test_aggiorna_spesa_id_non_esistente(tmp_path):
    percorso_db_tmp = tmp_path / "spese.db"
    crea_database(percorso_db_tmp)

    risultato = aggiorna_spesa(99, Spesa(
        "Benzina",
        "Auto",
        Decimal("50.00")
    ), percorso_db_tmp)

    assert risultato is False

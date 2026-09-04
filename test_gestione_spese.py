import pytest
import sqlite3
from main import mostra_totale, elabora_aggiungi_spesa
from spesa import Spesa
from gestione_spese import aggiungi_spesa, rimuovi_spesa
from unittest.mock import Mock
from decimal import Decimal
from database import crea_database, inserisci_spesa, leggi_spese

@pytest.fixture
def lista_spese():
    return [
        Spesa("Spesa 1", "Casa", Decimal("10.00"), 1),
        Spesa("Spesa 2", "Cibo", Decimal("20.00"), 2),
        Spesa("Spesa 3", "Svago", Decimal("15.00"), 3),
    ]

# TEST VISUALIZZAZIONE E CALCOLI

def test_mostra_totale(lista_spese):

    risultato = mostra_totale(lista_spese)

    assert risultato == 45

#TEST AGGIUNTA SPESA

def test_aggiungi_spesa(tmp_path):
    percorso_db_tmp = tmp_path / "spese.db"
    crea_database(percorso_db_tmp)

    spese = []

    aggiungi_spesa(spese, "Pizza", "Cibo", Decimal("12.00"), percorso_db_tmp)

    assert len(spese) == 1
    assert spese[0].descrizione == "Pizza"
    assert spese[0].categoria == "Cibo"
    assert spese[0].importo == Decimal("12.00")


def test_aggiungi_spesa_importo_negativo(lista_spese):

    with pytest.raises(ValueError):
        aggiungi_spesa(lista_spese, "Pizza", "Cibo", Decimal("-2.00"))

def test_aggiungi_spesa_descrizione_vuota(lista_spese):
    with pytest.raises(ValueError):
        aggiungi_spesa(lista_spese, "", "Cibo", Decimal("10.00"))

def test_aggiungi_spesa_categoria_vuota(lista_spese):
    with pytest.raises(ValueError):
        aggiungi_spesa(lista_spese, "Pizza", "", Decimal("10.00"))

def test_elabora_aggiungi_spesa(monkeypatch):
    spese = []

    input_simulato = iter(["Pizza", "Cibo", Decimal("10.00")])

    aggiungi_spesa_mock = Mock()

    monkeypatch.setattr("main.aggiungi_spesa", aggiungi_spesa_mock)

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(input_simulato)
    )

    elabora_aggiungi_spesa(spese)

    aggiungi_spesa_mock.assert_called_once_with(
        spese,
        "Pizza",
        "Cibo",
        Decimal("10.00")
    )

def test_aggiungi_spesa_errore(monkeypatch, capsys):
    spese = []

    input_simulato = iter(["Pizza", "Cibo", "abc"])

    aggiungi_spesa_mock = Mock()

    monkeypatch.setattr("main.aggiungi_spesa", aggiungi_spesa_mock)

    monkeypatch.setattr("builtins.input", lambda _: next(input_simulato))

    elabora_aggiungi_spesa(spese)

    aggiungi_spesa_mock.assert_not_called()

    captured = capsys.readouterr()

    assert "Inserisci una descrizione" in captured.out

#TEST VALIDAZIONE SPESA
def test_spesa_descrizione_solo_spazi():
    with pytest.raises(ValueError):
        Spesa("          ", "Cibo", Decimal("5.00"))

def test_spesa_categoria_solo_spazi():
    with pytest.raises(ValueError):
        Spesa("Pizza","          ", Decimal("5.00"))



# TEST OPERAZIONI DATABASE
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

    rimuovi_spesa(lista_spese, 2, percorso_db_tmp)

    spese_db = leggi_spese(percorso_db_tmp)

    assert len(lista_spese) == 2

    assert spese_db[0].id == lista_spese[0].id
    assert spese_db[0].descrizione == lista_spese[0].descrizione
    assert spese_db[0].categoria == lista_spese[0].categoria
    assert spese_db[0].importo == lista_spese[0].importo

    assert spese_db[1].id == lista_spese[1].id
    assert spese_db[1].descrizione == lista_spese[1].descrizione
    assert spese_db[1].categoria == lista_spese[1].categoria
    assert spese_db[1].importo == lista_spese[1].importo

def test_rimuovi_spesa_id_non_esistente(lista_spese, tmp_path):
    percorso_db_tmp = tmp_path / "spese.db"

    crea_database(percorso_db_tmp)

    for spesa in lista_spese:
        inserisci_spesa(spesa, percorso_db_tmp)

    rimuovi_spesa(lista_spese, 99, percorso_db_tmp)

    spese_db = leggi_spese(percorso_db_tmp)

    assert len(lista_spese) == 3
    assert len(spese_db) == 3

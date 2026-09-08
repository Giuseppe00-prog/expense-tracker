import pytest

from main import mostra_totale, elabora_aggiungi_spesa
from spesa import Spesa
from gestione_spese import aggiungi_spesa, rimuovi_spesa, modifica_spesa
from unittest.mock import Mock
from decimal import Decimal
from database import crea_database, inserisci_spesa

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

    nuova_spesa = aggiungi_spesa("Pizza", "Cibo", Decimal("12.00"), percorso_db_tmp)

    assert nuova_spesa.descrizione == "Pizza"
    assert nuova_spesa.categoria == "Cibo"
    assert nuova_spesa.importo == Decimal("12.00")


def test_aggiungi_spesa_importo_negativo():

    with pytest.raises(ValueError):
        aggiungi_spesa("Pizza", "Cibo", Decimal("-2.00"))

def test_aggiungi_spesa_descrizione_vuota():
    with pytest.raises(ValueError):
        aggiungi_spesa("", "Cibo", Decimal("10.00"))

def test_aggiungi_spesa_categoria_vuota():
    with pytest.raises(ValueError):
        aggiungi_spesa("Pizza", "", Decimal("10.00"))

def test_elabora_aggiungi_spesa(monkeypatch):

    input_simulato = iter(["Pizza", "Cibo", Decimal("10.00")])

    aggiungi_spesa_mock = Mock()

    monkeypatch.setattr("main.aggiungi_spesa", aggiungi_spesa_mock)

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(input_simulato)
    )

    elabora_aggiungi_spesa()

    aggiungi_spesa_mock.assert_called_once_with(
        "Pizza",
        "Cibo",
        Decimal("10.00")
    )

def test_aggiungi_spesa_errore(monkeypatch, capsys):

    input_simulato = iter(["Pizza", "Cibo", "abc"])

    aggiungi_spesa_mock = Mock()

    monkeypatch.setattr("main.aggiungi_spesa", aggiungi_spesa_mock)

    monkeypatch.setattr("builtins.input", lambda _: next(input_simulato))

    elabora_aggiungi_spesa()

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

#TEST MODIFICA SPESA
def test_modifica_spesa(tmp_path):
    percorso_db_tmp = tmp_path / "spese.db"
    crea_database(percorso_db_tmp)

    spesa_originale = Spesa(
        "Pizza",
        "Cibo",
        Decimal("12.50")
    )
    id_spesa = inserisci_spesa(spesa_originale, percorso_db_tmp)

    risultato = modifica_spesa(id_spesa, "Benzina", "Auto", Decimal("13.00"), percorso_db_tmp)

    assert risultato == Spesa(
        "Benzina",
        "Auto",
        Decimal("13.00"),
        id_spesa
    )

def test_modifica_spesa_id_non_valido(tmp_path):
    percorso_db_tmp = tmp_path / "spese.db"
    crea_database(percorso_db_tmp)

    risultato = modifica_spesa(99, "Benzina", "Auto", Decimal("13.00"), percorso_db_tmp)

    assert risultato is None
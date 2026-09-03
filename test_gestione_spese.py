import json
import pytest
from main import mostra_totale, elabora_aggiungi_spesa
from spesa import Spesa
from gestione_spese import aggiungi_spesa, rimuovi_spesa, salva_spese, carica_spese
from unittest.mock import Mock
from decimal import Decimal

@pytest.fixture
def lista_spese():
    return [
        Spesa("Spesa 1", "Casa", Decimal("10.00")),
        Spesa("Spesa 2", "Cibo", Decimal("20.00")),
        Spesa("Spesa 3", "Svago", Decimal("15.00")),
    ]

def test_mostra_totale(lista_spese):

    risultato = mostra_totale(lista_spese)

    assert risultato == 45

def test_aggiungi_spesa(monkeypatch, tmp_path):
    spese = []

    monkeypatch.setattr("gestione_spese.salva_spese", lambda spese, path: None)
    aggiungi_spesa(spese, "Pizza", "Cibo", Decimal("12.00"), tmp_path / 'spese.json')

    assert len(spese) == 1
    assert spese[0].descrizione == "Pizza"
    assert spese[0].categoria == "Cibo"
    assert spese[0].importo == Decimal("12.00")

def test_rimuovi_spesa(monkeypatch, lista_spese, tmp_path):

    monkeypatch.setattr("gestione_spese.salva_spese", lambda spese, path: None)
    rimuovi_spesa(lista_spese, 2, tmp_path / 'spese.json')
    assert len(lista_spese) == 2
    assert lista_spese[0].descrizione == "Spesa 1"
    assert lista_spese[1].descrizione == "Spesa 3"

def test_rimuovi_spesa_indice_non_valido(monkeypatch, lista_spese, tmp_path):

    monkeypatch.setattr("gestione_spese.salva_spese", lambda spese, path: None)

    with pytest.raises(ValueError):
        rimuovi_spesa(lista_spese, 0, tmp_path / 'spese.json')

    with pytest.raises(ValueError):
        rimuovi_spesa(lista_spese, 4, tmp_path / 'spese.json')

def test_salva_spesa(tmp_path, lista_spese):
    percorso_file = tmp_path / "spese.json"

    salva_spese(lista_spese, percorso_file)

    with open(percorso_file, "r") as file:
        spese_scritte = json.load(file)

    assert len(spese_scritte) == 3
    assert spese_scritte[0]["descrizione"] == "Spesa 1"
    assert spese_scritte[1]["descrizione"] == "Spesa 2"
    assert spese_scritte[2]["descrizione"] == "Spesa 3"

def test_carica_spesa(tmp_path):
    dati = [
        {
            "descrizione": "Spesa 1",
            "categoria": "Casa",
            "importo": "10.00"
        },
        {
            "descrizione": "Spesa 2",
            "categoria": "Cibo",
            "importo": "20.00"
        }
    ]

    percorso_file = tmp_path / "spese.json"

    with open(percorso_file, "w") as file:
        json.dump(dati, file)

    spese = carica_spese(percorso_file)

    assert len(spese) == 2
    assert isinstance(spese[0], Spesa)
    assert isinstance(spese[1], Spesa)
    assert spese[0].descrizione == "Spesa 1"
    assert spese[0].categoria == "Casa"
    assert spese[0].importo == Decimal("10.00")
    assert spese[1].descrizione == "Spesa 2"
    assert spese[1].categoria == "Cibo"
    assert spese[1].importo == Decimal("20.00")

def test_carica_spese_file_non_esistente(tmp_path):
    spese = carica_spese(tmp_path / "test.json")

    assert spese == []

def test_aggiungi_spesa_importo_negativo(lista_spese, tmp_path):
    with pytest.raises(ValueError):
        aggiungi_spesa(lista_spese, "Pizza", "Cibo", Decimal("-2.00"), tmp_path / 'spese.json')

def test_aggiungi_spesa_descrizione_vuota(lista_spese, tmp_path):
    with pytest.raises(ValueError):
        aggiungi_spesa(lista_spese, "", "Cibo", Decimal("10.00"), tmp_path / 'spese.json')

def test_aggiungi_spesa_categoria_vuota(lista_spese, tmp_path):
    with pytest.raises(ValueError):
        aggiungi_spesa(lista_spese, "Pizza", "", Decimal("10.00"), tmp_path / 'spese.json')

def test_spesa_descrizione_solo_spazi():
    with pytest.raises(ValueError):
        Spesa("          ", "Cibo", Decimal("5.00"))

def test_spesa_categoria_solo_spazi():
    with pytest.raises(ValueError):
        Spesa("Pizza","          ", Decimal("5.00"))

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
        Decimal("10.00"),
        "spese.json"
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
import pytest
from models.categoria import Categoria
from services.gestione_spese import aggiungi_spesa, modifica_spesa, recupera_spesa, elimina_spesa, SpesaNonTrovataError, \
    recupera_spese
from decimal import Decimal
from database import inserisci_categoria, recupera_categoria_per_nome


def test_aggiungi_spesa_categoria_esistente(database_test):
    categoria = Categoria("Test")
    categoria.id = inserisci_categoria(categoria)

    spesa = aggiungi_spesa("test", "Test", Decimal("12.50"))

    assert spesa.descrizione == "test"
    assert spesa.categoria == categoria
    assert spesa.importo == Decimal("12.50")

def test_aggiungi_spesa_categoria_non_esistente(database_test):
    spesa = aggiungi_spesa("test", "Test", Decimal("12.50"))

    assert spesa.descrizione == "test"
    assert spesa.categoria.nome == "Test"
    assert spesa.importo == Decimal("12.50")

def test_recupero_spesa_esistente(database_test):
    spesa = aggiungi_spesa("test", "Test", Decimal("12.50"))

    spesa_db = recupera_spesa(spesa.id)

    assert spesa_db is not None
    assert spesa == spesa_db

def test_recupero_spesa_non_esistente(database_test):
    with pytest.raises(Exception):
        recupera_spesa(99)

def test_recupero_spese(database_test):
    aggiungi_spesa("test", "Test", Decimal("12.50"))
    aggiungi_spesa("Prova", "Prova", Decimal("22.50"))

    lista_spese = recupera_spese()

    assert len(lista_spese) == 2

    descrizioni = [spesa.descrizione for spesa in lista_spese]

    assert "test" in descrizioni
    assert "Prova" in descrizioni


def test_elimina_spesa_esistente(database_test):
    spesa = aggiungi_spesa("test", "Test", Decimal("12.50"))

    risultato = elimina_spesa(spesa.id)

    assert risultato is True

    with pytest.raises(SpesaNonTrovataError):
        recupera_spesa(spesa.id)

def test_elimina_spesa_non_esistente(database_test):
    with pytest.raises(SpesaNonTrovataError):
        elimina_spesa(99)

def test_modifica_spesa_con_categoria_esistente(database_test):
    spesa = aggiungi_spesa("test", "Test", Decimal("12.50"))

    modifica_spesa(spesa.id, "Nuovo", "Test", Decimal("15.50"))

    spesa_db = recupera_spesa(spesa.id)

    assert spesa_db.importo == Decimal("15.50")
    assert spesa_db.id == spesa.id
    assert spesa_db.descrizione == "Nuovo"
    assert spesa_db.categoria == spesa.categoria

def test_modifica_spesa_con_categoria_non_esistente(database_test):
    spesa = aggiungi_spesa("test", "Test", Decimal("12.50"))

    modifica_spesa(spesa.id, "Nuovo", "Altro", Decimal("15.50"))

    spesa_db = recupera_spesa(spesa.id)

    assert spesa_db.importo == Decimal("15.50")
    assert spesa_db.id == spesa.id
    assert spesa_db.descrizione == "Nuovo"
    assert spesa_db.categoria.nome == "Altro"
    assert spesa_db.categoria.id is not None

    categoria_db = recupera_categoria_per_nome("Altro")

    assert categoria_db is not None
    assert spesa_db.categoria == categoria_db

def test_modifica_spesa_con_id_non_esistente(database_test):
    with pytest.raises(SpesaNonTrovataError):
        modifica_spesa(99, "Test", "Test", Decimal("12.50"))
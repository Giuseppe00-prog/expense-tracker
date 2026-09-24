import datetime
from decimal import Decimal
import pytest
from services.gestione_categorie import aggiungi_categoria, trova_categoria_tramite_id, trova_categoria_tramite_nome, recupera_categorie, modifica_categoria, \
    elimina_categoria, CategoriaDuplicataError, CategoriaNonTrovataError, CategoriaInUsoError
from services.gestione_spese import aggiungi_spesa

def test_aggiungi_categoria(database_test):
    categoria = aggiungi_categoria("Test")

    assert categoria.nome == "Test"

def test_aggiungi_categoria_già_esistente(database_test):
    aggiungi_categoria("Test")

    with pytest.raises(CategoriaDuplicataError):
        aggiungi_categoria("Test")

def test_recupero_categoria_per_id(database_test):
    categoria = aggiungi_categoria("Test")
    categoria = trova_categoria_tramite_id(categoria.id)
    assert categoria.nome == "Test"

def test_recupero_categoria_per_id_non_esistente(database_test):
    with pytest.raises(CategoriaNonTrovataError):
        trova_categoria_tramite_id(1234)

def test_recupero_categoria_per_nome(database_test):
    categoria = aggiungi_categoria("Test")
    categoria = trova_categoria_tramite_nome(categoria.nome)
    assert categoria.nome == "Test"

def test_recupero_categoria_per_nome_non_esistente(database_test):
    with pytest.raises(CategoriaNonTrovataError):
        trova_categoria_tramite_nome("1234")

def test_modifica_categoria(database_test):
    categoria = aggiungi_categoria("Test")
    categoria = trova_categoria_tramite_id(categoria.id)
    categoria.nome = "Modifica"
    categoria_modificata = modifica_categoria(categoria.id, categoria.nome)
    assert categoria_modificata.nome == "Modifica"

def test_modifica_categoria_duplicata(database_test):
    aggiungi_categoria("Test")
    categoria = aggiungi_categoria("Modifica")
    with pytest.raises(CategoriaDuplicataError):
        modifica_categoria(categoria.id, "Test")

def test_modifica_categoria_non_esistente(database_test):
    with pytest.raises(CategoriaNonTrovataError):
        modifica_categoria(1, "Test")

def test_elimina_categoria(database_test):
    categoria = aggiungi_categoria("Test")

    elimina_categoria(categoria.id)

    with pytest.raises(CategoriaNonTrovataError):
        trova_categoria_tramite_id(categoria.id)

def test_elimina_categoria_non_trovata(database_test):
    with pytest.raises(CategoriaNonTrovataError):
        elimina_categoria(1)

def test_elimina_categoria_in_uso(database_test):
    categoria = aggiungi_categoria("Test")
    aggiungi_spesa("Prova", "Test", Decimal("12.50"), datetime.date.today())
    with pytest.raises(CategoriaInUsoError):
        elimina_categoria(categoria.id)

def test_recupera_categorie(database_test):
    aggiungi_categoria("Test")
    aggiungi_categoria("Prova")

    lista_categorie = recupera_categorie()

    assert len(lista_categorie) == 2
    nomi = [categoria.nome for categoria in lista_categorie]

    assert "Test" in nomi
    assert "Prova" in nomi

import pytest
from sqlalchemy.exc import IntegrityError
from decimal import Decimal
from database import inserisci_categoria, recupera_categoria_per_id, recupera_categoria_per_nome, leggi_categorie, rimuovi_categoria, aggiorna_categoria, inserisci_spesa, leggi_spese, recupera_singola_spesa, aggiorna_spesa, rimuovi_spesa
from models.categoria import Categoria
from models.spesa import Spesa

#TEST CATEGORIA

def test_inserisci_categoria(database_test):
    categoria = Categoria(nome="Test2")

    id_categoria = inserisci_categoria(categoria)

    assert id_categoria is not None

    categoria_db = recupera_categoria_per_id(id_categoria)

    assert categoria_db.nome == categoria.nome
    assert categoria_db.id == id_categoria

def test_recupera_categoria_per_id_non_esistente(database_test):
    categoria_db = recupera_categoria_per_id(99)

    assert categoria_db is None

def test_recupera_categoria_per_nome(database_test):
    categoria = Categoria("Test3")

    id_categoria = inserisci_categoria(categoria)

    categoria_db = recupera_categoria_per_nome(categoria.nome)

    assert categoria_db.nome == categoria.nome
    assert categoria_db.id == id_categoria

def test_recupera_categoria_per_nome_non_esistente(database_test):
    categoria_db = recupera_categoria_per_nome("abc")

    assert categoria_db is None

def test_leggi_categorie(database_test):
    inserisci_categoria(Categoria("Cibo1"))
    inserisci_categoria(Categoria("Auto1"))

    categorie = leggi_categorie()

    assert len(categorie) == 2

    for categoria in categorie:
        assert isinstance(categoria, Categoria)

    nomi = [categoria.nome for categoria in categorie]

    assert "Cibo1" in nomi
    assert "Auto1" in nomi

def test_rimuovi_categoria(database_test):
    categoria = Categoria("Test4")

    id_categoria = inserisci_categoria(categoria)

    risultato = rimuovi_categoria(id_categoria)

    assert risultato

    categoria_db = recupera_categoria_per_id(id_categoria)

    assert categoria_db is None

def test_rimuovi_categoria_non_esistente(database_test):
    risultato = rimuovi_categoria(99)

    assert not risultato

def test_inserisci_categoria_duplicata(database_test):
    inserisci_categoria(Categoria("Test"))
    with pytest.raises(IntegrityError):
        inserisci_categoria(Categoria("Test"))

def test_aggiorna_categoria(database_test):
    id_categoria = inserisci_categoria(Categoria("Test"))
    assert aggiorna_categoria(Categoria(id = id_categoria, nome="Cibo"))

    categoria_db = recupera_categoria_per_id(id_categoria)

    assert categoria_db.nome == "Cibo"
def test_aggiorna_categoria_non_esistente(database_test):
    assert not aggiorna_categoria(Categoria(id=99, nome="Cibo"))

#TEST SPESA

def test_inserisci_spesa(database_test):
    categoria = Categoria("Cibo")
    id_categoria = inserisci_categoria(categoria)
    categoria.id = id_categoria

    spesa = Spesa(
        descrizione="Pizza",
        categoria=categoria,
        importo=Decimal("12.50")
    )

    id_spesa = inserisci_spesa(spesa)

    assert id_spesa > 0

def test_recupera_singola_spesa(database_test):
    categoria = Categoria("Cibo")
    id_categoria = inserisci_categoria(categoria)
    categoria.id = id_categoria

    spesa = Spesa(
        descrizione="Pizza",
        categoria=categoria,
        importo=Decimal("12.50")
    )
    id_spesa = inserisci_spesa(spesa)

    spesa_db = recupera_singola_spesa(id_spesa)

    assert spesa_db.id == id_spesa
    assert spesa_db.importo == Decimal("12.50")
    assert spesa_db.descrizione == "Pizza"
    assert spesa_db.categoria.id == id_categoria
    assert spesa_db.categoria.nome == "Cibo"

def test_recupera_singola_spesa_id_non_esistente(database_test):
    spesa_db = recupera_singola_spesa(99)
    assert spesa_db is None

def test_leggi_spese(database_test):
    categoria1 = Categoria("Cibo")
    id_categoria1 = inserisci_categoria(categoria1)
    categoria1.id = id_categoria1

    spesa1 = Spesa(
        descrizione="Pizza",
        categoria=categoria1,
        importo=Decimal("12.50")
    )
    id_spesa1 = inserisci_spesa(spesa1)

    categoria2 = Categoria("Macchina")
    id_categoria2 = inserisci_categoria(categoria2)
    categoria2.id = id_categoria2

    spesa2 = Spesa(
        descrizione="Benzina",
        categoria=categoria2,
        importo=Decimal("50.37")
    )
    id_spesa2 = inserisci_spesa(spesa2)

    lista_spese_db = leggi_spese()

    assert len(lista_spese_db) == 2

    ids = [spesa.id for spesa in lista_spese_db]

    assert id_spesa1 in ids
    assert id_spesa2 in ids

def test_rimuovi_spesa(database_test):
    categoria = Categoria("Cibo")
    id_categoria = inserisci_categoria(categoria)
    categoria.id = id_categoria

    spesa = Spesa(
        descrizione="Pizza",
        categoria=categoria,
        importo=Decimal("12.50")
    )
    id_spesa = inserisci_spesa(spesa)
    assert rimuovi_spesa(id_spesa)
    assert recupera_singola_spesa(id_spesa) is None

def test_rimuovi_spesa_non_esistente(database_test):
    assert not rimuovi_spesa(99)

def test_aggiorna_spesa(database_test):
    categoria_cibo = Categoria("Cibo")
    categoria_cibo.id = inserisci_categoria(categoria_cibo)

    categoria_svago = Categoria("Svago")
    categoria_svago.id = inserisci_categoria(categoria_svago)

    spesa = Spesa(
        descrizione="Pizza",
        categoria=categoria_cibo,
        importo=Decimal("12.50")
    )

    spesa.id = inserisci_spesa(spesa)

    spesa.descrizione = "Cinema"
    spesa.importo = Decimal("15.00")
    spesa.categoria = categoria_svago

    assert aggiorna_spesa(spesa)

    spesa_db = recupera_singola_spesa(spesa.id)

    assert spesa_db.descrizione == "Cinema"
    assert spesa_db.importo == Decimal("15.00")
    assert spesa_db.categoria.id == categoria_svago.id
    assert spesa_db.categoria.nome == "Svago"

def test_aggiorna_spesa_non_esistente(database_test):
    assert not aggiorna_spesa(Spesa(id=99, descrizione="Panino", categoria=Categoria(id=99, nome="Cibo"), importo=Decimal("12.50")))
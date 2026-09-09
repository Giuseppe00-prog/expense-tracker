import pytest
from decimal import Decimal
from models.spesa import Spesa
from models.categoria import Categoria

def test_spesa():
    categoria = Categoria("Cibo")
    spesa = Spesa("Pizza", categoria, Decimal("5.00"))

    assert isinstance(spesa, Spesa)
    assert spesa.descrizione == "Pizza"
    assert spesa.categoria == categoria
    assert spesa.importo == Decimal("5.00")
    assert categoria.id is None
    assert spesa.id is None

def test_spesa_descrizione_solo_spazi():
    with pytest.raises(ValueError):
        Spesa("          ", Categoria("Cibo"), Decimal("5.00"))

def test_spesa_importo_negativo():
    with pytest.raises(ValueError):
        Spesa("Pizza",Categoria("Cibo"), Decimal("-5.00"))
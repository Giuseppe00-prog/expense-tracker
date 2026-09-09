import pytest
from models.categoria import Categoria

def test_categoria():
    categoria = Categoria("Cibo")

    assert isinstance(categoria, Categoria) is True
    assert categoria.nome == "Cibo"

def test_nome_categoria_vuoto():
    with pytest.raises(ValueError):
        Categoria("    ")
from psycopg.errors import ForeignKeyViolation

from database import recupera_categoria_per_nome, inserisci_categoria, recupera_categoria_per_id, aggiorna_categoria, leggi_categorie, rimuovi_categoria
from models.categoria import Categoria


class CategoriaNonTrovataError(Exception):
    pass

class CategoriaDuplicataError(Exception):
    pass

class CategoriaInUsoError(Exception):
    pass

def aggiungi_categoria(nome):
    """Crea e restituisce una nuova categoria se il nome non è già utilizzato."""
    categoria = recupera_categoria_per_nome(nome)
    if categoria is not None:
        raise CategoriaDuplicataError("La categoria {} già esiste".format(nome))

    categoria = Categoria(nome)
    categoria.id = inserisci_categoria(categoria)

    return categoria

def trova_categoria_tramite_id(id_categoria):
    """Recupera una categoria tramite id o solleva un errore se non esiste."""
    risultato = recupera_categoria_per_id(id_categoria)

    if not risultato:
        raise CategoriaNonTrovataError("La categoria con id {} non esiste".format(id_categoria))

    return risultato

def trova_categoria_tramite_nome(nome):
    """Recupera una categoria tramite nome o solleva un errore se non esiste."""
    risultato = recupera_categoria_per_nome(nome)

    if not risultato:
        raise CategoriaNonTrovataError("La categoria con nome {} non esiste".format(nome))

    return risultato

def modifica_categoria(id_categoria, nome):
    """Modifica il nome di una categoria esistente."""
    categoria_attuale = recupera_categoria_per_id(id_categoria)

    if categoria_attuale is None:
        raise CategoriaNonTrovataError(
            f"La categoria con id {id_categoria} non esiste"
        )

    categoria_stesso_nome = recupera_categoria_per_nome(nome)

    if (
        categoria_stesso_nome is not None
        and categoria_stesso_nome.id != id_categoria
    ):
        raise CategoriaDuplicataError(
            f"La categoria {nome} esiste già"
        )

    categoria = Categoria(
        id=id_categoria,
        nome=nome
    )

    aggiorna_categoria(categoria)

    return categoria

def elimina_categoria(id_categoria):
    """Elimina la categoria se esiste tramite id_categoria"""
    categoria = recupera_categoria_per_id(id_categoria)
    if categoria is None:
        raise CategoriaNonTrovataError("La categoria con id {} non esiste".format(id_categoria))
    try:
        return rimuovi_categoria(id_categoria)
    except ForeignKeyViolation:
        raise CategoriaInUsoError(
            "La categoria {} non può essere eliminata perché è utilizzata da una o più spese"
        )

def recupera_categorie():
    """Recupera tutte le categorie salvate a db"""
    return leggi_categorie()

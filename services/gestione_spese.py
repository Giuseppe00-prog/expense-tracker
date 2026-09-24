"""Funzioni per la gestione delle spese."""

from database import (
    inserisci_spesa,
    rimuovi_spesa,
    recupera_singola_spesa,
    aggiorna_spesa, leggi_spese
)
from models.spesa import Spesa
from services.gestione_categorie import (
    aggiungi_categoria,
    trova_categoria_tramite_nome,
    CategoriaNonTrovataError
)


class SpesaNonTrovataError(Exception):
    pass


def aggiungi_spesa(descrizione, nome_categoria, importo, data):
    try:
        categoria = trova_categoria_tramite_nome(nome_categoria)
    except CategoriaNonTrovataError:
        categoria = aggiungi_categoria(nome_categoria)

    nuova_spesa = Spesa(
        descrizione,
        categoria,
        importo,
        data
    )
    nuova_spesa.id = inserisci_spesa(nuova_spesa)
    return nuova_spesa

def elimina_spesa(id_spesa):
    """Rimuove una spesa dal database tramite il suo id."""
    risultato = rimuovi_spesa(id_spesa)

    if not risultato:
        raise SpesaNonTrovataError("L'id spesa non è associato a nessuna spesa esistente")

    return risultato

def recupera_spesa(id_spesa):
    risultato = recupera_singola_spesa(id_spesa)

    if not risultato:
        raise SpesaNonTrovataError("L'id spesa non è associato a nessuna spesa esistente")

    return risultato

def recupera_spese():
    return leggi_spese()

def modifica_spesa(id_spesa, descrizione, nome_categoria, importo, data):
    if recupera_singola_spesa(id_spesa) is None:
        raise SpesaNonTrovataError("L'id spesa non è associato a nessuna spesa esistente")

    try:
        categoria = trova_categoria_tramite_nome(nome_categoria)
    except CategoriaNonTrovataError:
        categoria = aggiungi_categoria(nome_categoria)

    spesa = Spesa(
        descrizione,
        categoria,
        importo,
        data,
        id = id_spesa
    )
    aggiorna_spesa(spesa)

    return spesa
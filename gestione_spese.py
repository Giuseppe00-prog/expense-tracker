"""Funzioni per la gestione delle spese."""

from database import inserisci_spesa, rimuovi_spesa, recupera_singola_spesa as elimina_dal_database, \
    recupera_singola_spesa
from spesa import Spesa


def aggiungi_spesa(descrizione, categoria, importo, percorso_spesa="spese.db"):
    """Crea una nuova spesa, la salva nel database e la aggiunge alla lista."""
    nuova_spesa = Spesa(descrizione, categoria, importo)

    id_nuova_spesa = inserisci_spesa(nuova_spesa, percorso_spesa)

    nuova_spesa.id = id_nuova_spesa

    return nuova_spesa

def rimuovi_spesa(id_spesa, percorso_spesa="spese.db"):
    """Rimuove una spesa dal database tramite il suo id."""
    return elimina_dal_database(id_spesa, percorso_spesa)

def recupera_spesa(id_spesa, percorso_spesa="spese.db"):
    return recupera_singola_spesa(id_spesa, percorso_spesa)


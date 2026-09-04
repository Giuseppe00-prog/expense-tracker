"""Funzioni per la gestione delle spese."""

from database import inserisci_spesa, rimuovi_spesa as elimina_dal_database
from spesa import Spesa


def aggiungi_spesa(spese, descrizione, categoria, importo, percorso_spesa="spese.db"):
    """Crea una nuova spesa, la salva nel database e la aggiunge alla lista."""
    nuova_spesa = Spesa(descrizione, categoria, importo)

    id_nuova_spesa = inserisci_spesa(nuova_spesa, percorso_spesa)

    nuova_spesa.id = id_nuova_spesa

    spese.append(nuova_spesa)

def rimuovi_spesa(spese, id_spesa, percorso_spesa="spese.db"):
    """Rimuove una spesa dalla lista e dal database tramite il suo id."""
    esiste_id = False
    for spesa in spese:
        if spesa.id == id_spesa:
            spese.remove(spesa)
            esiste_id = True
            break
    if esiste_id:
        elimina_dal_database(id_spesa, percorso_spesa)


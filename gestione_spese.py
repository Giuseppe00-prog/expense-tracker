from spesa import Spesa
import json
from dataclasses import asdict
from decimal import Decimal

def salva_spese(spese, path):
    spese_dictionary = [{**asdict(spesa), "importo": str(spesa.importo) } for spesa in spese]
    with open(path, 'w') as file:
        json.dump(spese_dictionary, file, indent=4)

def carica_spese(path):
    try:
        with open(path, 'r') as file:
            dati = json.load(file)
            lista_spese = [
                Spesa(
                    descrizione=spesa["descrizione"],
                    categoria=spesa["categoria"],
                    importo=Decimal(str(spesa["importo"]))
                      )
                for spesa in dati
            ]
            return lista_spese
    except FileNotFoundError:
        return []

def aggiungi_spesa(spese, descrizione, categoria, importo, path):
    spese.append(Spesa(descrizione, categoria, importo))
    salva_spese(spese, path)

def rimuovi_spesa(spese, indice, path):
    if not 1 <= indice <= len(spese):
        raise ValueError('Indice della spesa non valido')
    spese.remove(spese[indice - 1])
    salva_spese(spese, path)

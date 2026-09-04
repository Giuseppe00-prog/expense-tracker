"""Interfaccia a riga di comando per la gestione delle spese."""

from gestione_spese import aggiungi_spesa, rimuovi_spesa
from decimal import Decimal, InvalidOperation
from database import leggi_spese

lista_spese = leggi_spese()

def mostra_spese(spese):
    """Restituisce l'elenco delle spese formattato per la visualizzazione."""
    righe = [
        f"{indice}. {spesa.descrizione} | {spesa.categoria} | {spesa.importo} €"
        for indice, spesa in enumerate(spese, start=1)
    ]
    return "\n".join(righe)

def mostra_totale(spese):
    """Calcola e restituisce il totale degli importi delle spese."""
    totale = sum(spesa.importo for spesa in spese)
    return totale

def elabora_mostra_spese(spese):
    """Visualizza l'elenco delle spese nel terminale."""
    print('--- SPESE --- \n')
    print(mostra_spese(spese))

def elabora_mostra_totale(spese):
    """Visualizza nel terminale il totale delle spese."""
    print(mostra_totale(spese))

def elabora_aggiungi_spesa(spese):
    """Acquisisce i dati dall'utente e aggiunge una nuova spesa."""
    descrizione = input("Descrizione: ")
    categoria = input("Categoria: ")
    try:
        importo = Decimal(input("Importo: "))
        aggiungi_spesa(spese, descrizione, categoria, importo)
        print('Spesa aggiunta con successo')
    except (ValueError, InvalidOperation):
        print('Inserisci una descrizione e una categoria valida e un importo non negativo')

def elabora_rimuovi_spesa(spese):
    """Mostra le spese e gestisce la rimozione di quella selezionata dall'utente."""
    elabora_mostra_spese(spese)
    try:
        indice_spesa_da_rimuovere = int(input('Quale spesa vuoi rimuovere? '))
        if not 1 <= indice_spesa_da_rimuovere <= len(spese):
            raise ValueError('Inserisci un numero valido')
        rimuovi_spesa(spese, spese[indice_spesa_da_rimuovere - 1].id)
        print('Spesa rimossa con successo')
    except ValueError:
        print('Inserisci un numero valido')

def menu(spese):
    """Visualizza il menu principale e gestisce la scelta dell'utente."""
    print('=== EXPENSE TRACKER ===\n')
    print('1. Aggiungi spesa')
    print('2. Mostra spese')
    print('3. Mostra totale')
    print('4. Rimuovi Spesa')
    print('5. Esci')
    try:
        numero_scelto = int(input('Scelta: '))
        if numero_scelto < 1 or numero_scelto > 5:
            print('Inserisci un numero valido')
            return -1
        else:
            match numero_scelto:
                case 1:
                    elabora_aggiungi_spesa(spese)
                case 2:
                    elabora_mostra_spese(spese)
                case 3:
                    elabora_mostra_totale(spese)
                case 4:
                    elabora_rimuovi_spesa(spese)
            return numero_scelto
    except ValueError:
        print('Inserisci un numero valido')
        return -1

if __name__ == '__main__':
    while True:
        scelta = menu(lista_spese)
        if scelta == 5:
            break

    print('Arrivederci')
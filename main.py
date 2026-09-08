"""Interfaccia a riga di comando per la gestione delle spese."""

from gestione_spese import aggiungi_spesa, rimuovi_spesa
from decimal import Decimal, InvalidOperation
from database import leggi_spese, crea_database


def mostra_spese(spese):
    """Restituisce l'elenco delle spese formattato per la visualizzazione."""
    righe = [
        f"{indice}. {spesa.descrizione} | {spesa.categoria} | {spesa.importo} €"
        for indice, spesa in enumerate(spese, start=1)
    ]
    return "\n".join(righe)

def mostra_totale(spese):
    """Calcola e restituisce il totale degli importi delle spese."""
    return sum(spesa.importo for spesa in spese)

def elabora_mostra_spese():
    """Visualizza l'elenco delle spese nel terminale."""
    spese = leggi_spese()
    print('--- SPESE --- \n')
    print(mostra_spese(spese))

def elabora_mostra_totale():
    """Visualizza nel terminale il totale delle spese."""
    spese = leggi_spese()
    print(mostra_totale(spese))

def elabora_aggiungi_spesa():
    """Acquisisce i dati dall'utente e aggiunge una nuova spesa."""
    descrizione = input("Descrizione: ")
    categoria = input("Categoria: ")
    try:
        importo = Decimal(input("Importo: "))
        aggiungi_spesa(descrizione, categoria, importo)
        print('Spesa aggiunta con successo')
    except (ValueError, InvalidOperation):
        print('Inserisci una descrizione e una categoria valida e un importo non negativo')

def elabora_rimuovi_spesa():
    """Mostra le spese e gestisce la rimozione di quella selezionata dall'utente."""
    spese = leggi_spese()
    print('--- SPESE --- \n')
    print(mostra_spese(spese))

    try:
        indice_spesa_da_rimuovere = int(input('Quale spesa vuoi rimuovere? '))
        if not 1 <= indice_spesa_da_rimuovere <= len(spese):
            raise ValueError('Inserisci un numero valido')
        spesa_rimossa = rimuovi_spesa(spese[indice_spesa_da_rimuovere - 1].id)
        if spesa_rimossa:
            print('Spesa rimossa con successo')
        else:
            print("La spesa non è stata rimossa")
    except ValueError:
        print('Inserisci un numero valido')

def menu():
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
                    elabora_aggiungi_spesa()
                case 2:
                    elabora_mostra_spese()
                case 3:
                    elabora_mostra_totale()
                case 4:
                    elabora_rimuovi_spesa()
            return numero_scelto
    except ValueError:
        print('Inserisci un numero valido')
        return -1

if __name__ == '__main__':
    crea_database()
    while True:
        scelta = menu()
        if scelta == 5:
            break

    print('Arrivederci')
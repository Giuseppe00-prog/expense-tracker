from gestione_spese import carica_spese, aggiungi_spesa, rimuovi_spesa
from decimal import Decimal, InvalidOperation

lista_spese = carica_spese('spese.json')

def mostra_spese(spese):
    righe = [
        f"{indice}. {spesa.descrizione} | {spesa.categoria} | {spesa.importo} €"
        for indice, spesa in enumerate(spese, start=1)
    ]
    return "\n".join(righe)

def mostra_totale(spese):
    totale = sum(spesa.importo for spesa in spese)
    return totale

def elabora_mostra_spese(spese):
    print('--- SPESE --- \n')
    print(mostra_spese(spese))

def elabora_mostra_totale(spese):
    print(mostra_totale(spese))

def elabora_aggiungi_spesa(spese):
    descrizione = input("Descrizione: ")
    categoria = input("Categoria: ")
    try:
        importo = Decimal(input("Importo: "))
        aggiungi_spesa(spese, descrizione, categoria, importo, 'spese.json')
        print('Spesa aggiunto con successo')
    except ValueError, InvalidOperation:
        print('Inserisci una descrizione e una categoria valida e un importo non negativo')

def elabora_rimuovi_spesa(spese):
    elabora_mostra_spese(spese)
    try:
        indice_spesa_da_rimuovere = int(input('Quale spesa vuoi rimuovere? '))
        rimuovi_spesa(spese, indice_spesa_da_rimuovere, 'spese.json')
        print('Spesa rimossa con successo')
    except ValueError:
        print('Inserisci un numero valido')

def menu(spese):
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
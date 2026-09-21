import type {NuovaSpesa, Spesa, RispostaCreazioneSpesa} from "../types/Spesa"
import type {Categoria} from "../types/Categoria.ts";

const API_URL = import.meta.env.VITE_API_URL

export async function getSpese(): Promise<Spesa[]> {
    const response = await fetch(`${API_URL}/spese`)
    if(!response.ok) {
        throw new Error(`Errore HTTP: ${response.status}`)
    }
    return response.json()

}

export async function creaSpesa(nuovaSpesa: NuovaSpesa): Promise<Spesa> {
    const response = await fetch(`${API_URL}/spese`, {
        method:'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(nuovaSpesa)
    })
    if(!response.ok) {
        throw new Error(`Errore HTTP: ${response.status}`)
    }
    const jsonRisposta: RispostaCreazioneSpesa = await response.json()
    const spesaCreata: Spesa = {
        id: jsonRisposta.id,
        ...nuovaSpesa
    }
    return spesaCreata
}

export async function rimuoviSpesa(id: number): Promise<void> {
    const risposta = await fetch(`${API_URL}/spese/${id}`, {
    method:'DELETE'
    })

    if(!risposta.ok) {
        throw new Error(`Errore HTTP: ${risposta.status}`)
    }
}

export async function aggiornaSpesa(id: number, spesaModificata: NuovaSpesa): Promise<void> {
    const risposta = await fetch(`${API_URL}/spese/${id}`, {
        method:'PUT',
        headers: {
            'Content-Type' : 'application/json'
        },
        body: JSON.stringify(spesaModificata)
    })

    if(!risposta.ok) {
        throw new Error(`Errore HTTP: ${risposta.status}`)
    }
}

export async function getCategorie(): Promise<Categoria[]> {
    const response = await fetch(`${API_URL}/categorie`)

    if(!response.ok) {
        throw new Error(`Errore HTTP: ${response.status}`)
    }

    return response.json()
}
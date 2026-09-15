export type Spesa = {
    id: number
    descrizione: string
    categoria: string
    importo: number
}

export type NuovaSpesa = {
    descrizione: string
    categoria: string
    importo: number
}

export type RispostaCreazioneSpesa = {
    message: string
    id: number
}
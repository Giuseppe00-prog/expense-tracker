export type Spesa = {
    id: number
    descrizione: string
    categoria: string
    importo: number,
    data: string
}

export type NuovaSpesa = {
    descrizione: string
    categoria: string
    importo: number,
    data: string
}

export type RispostaCreazioneSpesa = {
    message: string
    id: number
}
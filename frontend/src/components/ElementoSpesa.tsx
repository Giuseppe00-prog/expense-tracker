import type {NuovaSpesa,Spesa as SpesaType} from '../types/Spesa'
import {useState} from "react";

type ElementoSpesaProps = SpesaType & {
    onEliminaSpesa: (id:number) => Promise<boolean>,
    onModificaSpesa: (id:number, spesa: NuovaSpesa) => Promise<boolean>
}

function ElementoSpesa({id, descrizione, categoria, importo, onEliminaSpesa, onModificaSpesa}: ElementoSpesaProps) {
    const [eliminazione, setEliminazione] = useState(false)
    const [errore, setErrore] = useState('')
    const [modifica, setModifica] = useState(false)
    const [descrizioneModificata, setDescrizioneModificata] = useState(descrizione)
    const [categoriaModificata, setCategoriaModificata] = useState(categoria)
    const [importoModificato, setImportoModificato] = useState(importo.toString())
    const [salvataggioModifica, setSalvataggioModifica] = useState(false)

    function annullaModifica() {
        setDescrizioneModificata(descrizione)
        setCategoriaModificata(categoria)
        setImportoModificato(importo.toString())
        setErrore('')
        setModifica(false)
    }

    async function handleElimina() {
        setEliminazione(true)
        setErrore('')
        try {
            const eliminazioneRiuscita = await onEliminaSpesa(id)

            if (!eliminazioneRiuscita) {
                setErrore('Impossibile eliminare la spesa')
            }
        }
        finally {
            setEliminazione(false)
    }
    }
    async function handleModifica() {
        if (
            descrizioneModificata.trim() === '' ||
            categoriaModificata.trim() === '' ||
            Number(importoModificato) <= 0
        ) {
            setErrore('Compila tutti i campi correttamente')
            return
        }

        const spesaModificata: NuovaSpesa = {
            descrizione: descrizioneModificata,
            categoria: categoriaModificata,
            importo: Number(importoModificato)
        }

        setSalvataggioModifica(true)
        setErrore('')

        try {
            const modificaRiuscita = await onModificaSpesa(id, spesaModificata)

            if (modificaRiuscita) {
                setDescrizioneModificata(spesaModificata.descrizione)
                setCategoriaModificata(spesaModificata.categoria)
                setImportoModificato(spesaModificata.importo.toString())
                setModifica(false)
            } else {
                setErrore('Impossibile modificare la spesa')
            }
        }
        finally {
            setSalvataggioModifica(false)
        }
    }
    return (
        <>
            {!modifica ? (
                <>
                    <p>
                        Descrizione - {descrizione}
                        <br/>
                        Categoria - {categoria}
                        <br/>
                        Importo - {importo.toFixed(2)} €
                    </p>
                    <button onClick={() => setModifica(true)}>
                        Modifica
                    </button>
                    <button onClick={() => void handleElimina()} disabled={eliminazione}>{eliminazione ? 'Eliminazione ...' : 'Elimina'}</button>
                    {errore && <p>{errore}</p>}
                </>
            ): (
                <>
                    <input
                        value={descrizioneModificata}
                        onChange={(event) => setDescrizioneModificata(event.target.value)}
                    />
                    <input
                        value={categoriaModificata}
                        onChange={(event)=>setCategoriaModificata(event.target.value)}
                    />
                    <input
                        type="number"
                        min="0.01"
                        step="0.01"
                        value={importoModificato}
                        onChange={(event) => setImportoModificato(event.target.value)}
                    />

                    <button
                        onClick={() => void handleModifica()}
                        disabled={salvataggioModifica}
                    >
                        {salvataggioModifica ? 'Salvataggio...' : 'Salva'}
                    </button>

                    <button onClick={annullaModifica}>
                        Annulla
                    </button>
                </>
            )}
        </>
    )
}

export default ElementoSpesa
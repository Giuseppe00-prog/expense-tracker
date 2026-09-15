import {useState, type SyntheticEvent} from 'react'
import type {NuovaSpesa} from "../types/Spesa";

type FormSpesaProps = {
    onAggiungiSpesa: (spesa: NuovaSpesa) => Promise<boolean>
}

function FormSpesa({onAggiungiSpesa}: FormSpesaProps) {
    const [descrizione, setDescrizione] = useState('')
    const [categoria, setCategoria] = useState('')
    const [importo, setImporto] = useState('')
    const [errore, setErrore] = useState('')
    const [salvataggio, setSalvataggio] = useState(false)

    async function handleSubmit(event: SyntheticEvent<HTMLFormElement, SubmitEvent>) {
        event.preventDefault()
        if (
            descrizione.trim() === '' ||
            categoria.trim() === '' ||
            Number(importo) <= 0
         ) {
            setErrore('Compila tutti i campi correttamente')
            return
        }

        const nuovaSpesa: NuovaSpesa = {
            descrizione: descrizione,
            categoria: categoria,
            importo: Number(importo)
        }

        setSalvataggio(true)
        try {
            const aggiuntaRiuscita = await onAggiungiSpesa(nuovaSpesa)
            if (aggiuntaRiuscita) {
                setDescrizione('')
                setCategoria('')
                setImporto('')
                setErrore('')
            } else {
                setErrore('Errore durante il salvataggio della spesa')
            }
        }
        finally {
            setSalvataggio(false)
        }
    }


    return (
        <>
            <h2>Nuova spesa</h2>

            <form onSubmit={handleSubmit}>
                <label htmlFor='descrizione'>Descrizione</label>
                <input required id='descrizione' value={descrizione} onChange={(event) => setDescrizione(event.target.value)}/>
                <label htmlFor='categoria'>Categoria</label>
                <input required id='categoria' value={categoria} onChange={(event) => setCategoria(event.target.value)} />
                <label htmlFor='importo'>Importo</label>
                <input required id='importo' min='0.01' step='0.01' type='number' value={importo} onChange={(event) => setImporto(event.target.value)} />
                <button type="submit" disabled={salvataggio}>Aggiungi spesa</button>
            </form>

            {errore && <p>{errore}</p>}
        </>
    )
}
export default FormSpesa
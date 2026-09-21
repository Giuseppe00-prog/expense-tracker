import {useState, type SyntheticEvent} from 'react'
import type {NuovaSpesa} from "../types/Spesa";
import type {Categoria} from "../types/Categoria.ts";

type FormSpesaProps = {
    onAggiungiSpesa: (spesa: NuovaSpesa) => Promise<boolean>
    categorie: Categoria[]
}

function FormSpesa({onAggiungiSpesa, categorie}: FormSpesaProps) {
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
                <select required value={categoria} onChange={(event) => setCategoria(event.target.value)}>
                    <option value="">Seleziona una categoria</option>
                    {
                    categorie.map(categoria =>
                        <option key={categoria.id} value={categoria.nome}>{categoria.nome}</option>
                    )
                    }
                </select>
                <label htmlFor='importo'>Importo</label>
                <input required id='importo' min='0.01' step='0.01' type='number' value={importo} onChange={(event) => setImporto(event.target.value)} />
                <button type="submit" disabled={salvataggio}>Aggiungi spesa</button>
            </form>

            {errore && <p>{errore}</p>}
        </>
    )
}
export default FormSpesa
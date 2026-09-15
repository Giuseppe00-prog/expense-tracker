import {useState, useEffect} from 'react'
import './App.css'
import Header from "./components/Header";
import type {NuovaSpesa, Spesa} from "./types/Spesa"
import ListaSpese from "./components/ListaSpese"
import FormSpesa from "./components/FormSpesa";
import {getSpese, creaSpesa, rimuoviSpesa, aggiornaSpesa} from "./services/api";

function App() {
    const [spese, setSpese] = useState<Spesa[]>([])
    const [caricamento, setCaricamento] = useState(true)
    const [erroreCaricamento, setErroreCaricamento] = useState('')

  async function aggiungiSpesa(nuovaSpesa: NuovaSpesa): Promise<boolean> {
        try {
            const spesaCreata = await creaSpesa(nuovaSpesa)
            setSpese(prevSpese => [...prevSpese, spesaCreata])

            return true
        }
        catch (errore) {
            console.error('Errore durante aggiunta spesa:', errore)
            return false
        }

  }

  async function eliminaSpesa(id: number): Promise<boolean> {
        try {
            await rimuoviSpesa(id)

            setSpese(prevSpese => prevSpese.filter(spesa => spesa.id !== id))

            return true
        }
        catch (errore) {
            console.error('Errore durante eliminazione spesa:', errore)
            return false
        }
  }

  async function modificaSpesa(id: number, spesaModificata: NuovaSpesa): Promise<boolean> {
        try {
            await aggiornaSpesa(id, spesaModificata)

            setSpese(prevSpese => prevSpese.map(spesa =>
                spesa.id === id ? {
                    id:id,
                    ...spesaModificata
                } : spesa
            ))

            return true
        }
        catch (errore) {
            console.error('Errore durante modifica spesa:', errore)
            return false
        }
  }
  useEffect(() => {
      async function caricaSpese() {
        try {
            const dati = await getSpese()
            setSpese(dati)
        }
        catch (errore){
            console.error('Errore durante il caricamento delle spese:', errore)
            setErroreCaricamento('Impossibile caricare le spese')
        }
        finally {
            setCaricamento(false)
        }
      }
      void caricaSpese()
  }, [])
  return (
    <>
      <Header titolo='Gestione spese' sottotitolo='Gestisci le tue spese in modo semplice'/>
        {caricamento ? (
            <p>Caricamento spese...</p>
        ): erroreCaricamento ? (
            <p>{erroreCaricamento}</p>
            ): (
            <ListaSpese spese={spese} onEliminaSpesa={eliminaSpesa} onModificaSpesa={modificaSpesa}/>
        )}
      <FormSpesa onAggiungiSpesa={aggiungiSpesa}/>
    </>
  )
}


export default App

import type {NuovaSpesa, Spesa} from '../types/Spesa'
import ElementoSpesa from './ElementoSpesa'
type ListaSpeseProps = {
    spese: Spesa[],
    onEliminaSpesa: (id: number) => Promise<boolean>,
    onModificaSpesa: (id: number, spesa: NuovaSpesa) => Promise<boolean>
}

function ListaSpese({spese, onEliminaSpesa, onModificaSpesa}: ListaSpeseProps) {
    return (
        <>
            <h2>Le mie spese</h2>
            {
                spese.length === 0 ? (
                    <p>Nessuna spesa presente.</p>
                ) : (
                    spese.map(spesa => <ElementoSpesa key={spesa.id} id={spesa.id} descrizione={spesa.descrizione} categoria={spesa.categoria} importo={spesa.importo} onEliminaSpesa={onEliminaSpesa} onModificaSpesa={onModificaSpesa}/>)
                )
            }
        </>
    )
}

export default ListaSpese
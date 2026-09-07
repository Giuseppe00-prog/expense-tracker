from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import leggi_spese
from decimal import Decimal
from gestione_spese import aggiungi_spesa, rimuovi_spesa, recupera_spesa

app = FastAPI()

class SpesaRequest(BaseModel):
    descrizione: str
    categoria: str
    importo: Decimal

class SpesaResponse(BaseModel):
    message: str
    id: int

class SpesaResponseData(BaseModel):
    id: int
    descrizione: str
    categoria: str
    importo: Decimal
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/spese", response_model=list[SpesaResponseData])
def recupero_spese_api():
    return leggi_spese()


@app.post("/spese", status_code=201, response_model=SpesaResponse)
def aggiungi_spesa_api(spesa: SpesaRequest):
    nuova_spesa = aggiungi_spesa(spesa.descrizione, spesa.categoria, spesa.importo)
    return {
        "message": "Spesa aggiunta con successo",
        "id": nuova_spesa.id
    }

@app.delete("/spese/{id_spesa}", response_model=SpesaResponse)
def elimina_spesa_api(id_spesa: int):
    spesa_rimossa = rimuovi_spesa(id_spesa)
    if spesa_rimossa:
        return {
            "message": "Spesa rimossa",
            "id": id_spesa
        }
    else:
        raise HTTPException(
            status_code=404,
            detail="La spesa con l'id indicato non esiste",
        )

@app.get("/spese/{id_spesa}", response_model=SpesaResponseData)
def recupera_spesa_api(id_spesa: int):
    spesa = recupera_spesa(id_spesa)
    if spesa is None:
        raise HTTPException(
            status_code=404,
            detail="La spesa non esiste"
        )
    return spesa
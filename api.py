from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
from database import leggi_spese, crea_database
from decimal import Decimal
from gestione_spese import aggiungi_spesa, rimuovi_spesa, recupera_spesa, modifica_spesa
from contextlib import asynccontextmanager
from pydantic_core import PydanticCustomError

PERCORSO_DATABASE = "spese.db"

@asynccontextmanager
async def lifespan(app: FastAPI):
    crea_database(PERCORSO_DATABASE)

    yield
app = FastAPI(lifespan=lifespan)

class SpesaRequest(BaseModel):
    descrizione: str
    categoria: str
    importo: Decimal

    @field_validator("descrizione", "categoria")
    @classmethod
    def valida_testo(cls, valore):
        valore = valore.strip()

        if valore == "":
            raise PydanticCustomError(
                "descrizione_o_categoria_vuota",
                "La descrizione e la categoria non possono essere vuote"
            )

        return valore

    @field_validator("importo")
    @classmethod
    def valida_importo(cls, valore):
        if valore < 0:
            raise PydanticCustomError(
                "importo_negativo",
                "L'importo non può essere negativo"
            )

        return valore

class SpesaResponse(BaseModel):
    message: str
    id: int

class SpesaResponseData(BaseModel):
    id: int
    descrizione: str
    categoria: str
    importo: float
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/spese", response_model=list[SpesaResponseData])
def recupero_spese_api():
    return leggi_spese(PERCORSO_DATABASE)


@app.post("/spese", status_code=201, response_model=SpesaResponse)
def aggiungi_spesa_api(spesa: SpesaRequest):
    nuova_spesa = aggiungi_spesa(spesa.descrizione, spesa.categoria, spesa.importo, PERCORSO_DATABASE)
    return {
        "message": "Spesa aggiunta con successo",
        "id": nuova_spesa.id
    }

@app.delete("/spese/{id_spesa}", response_model=SpesaResponse)
def elimina_spesa_api(id_spesa: int):
    spesa_rimossa = rimuovi_spesa(id_spesa, PERCORSO_DATABASE)
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
    spesa = recupera_spesa(id_spesa, PERCORSO_DATABASE)
    if spesa is None:
        raise HTTPException(
            status_code=404,
            detail="La spesa non esiste"
        )
    return spesa

@app.put("/spese/{id_spesa}", response_model=SpesaResponseData)
def modifica_spesa_api(id_spesa: int, spesa: SpesaRequest):
    spesa_aggiornata = modifica_spesa(
        id_spesa,
        spesa.descrizione,
        spesa.categoria,
        spesa.importo,
        PERCORSO_DATABASE
    )
    if spesa_aggiornata is None:
        raise HTTPException(
            status_code=404,
            detail = "La spesa non esiste"
        )
    return spesa_aggiornata


from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
from decimal import Decimal
from services.gestione_spese import (
    aggiungi_spesa,
    recupera_spesa,
    modifica_spesa,
    elimina_spesa,
    recupera_spese, SpesaNonTrovataError
)
from services.gestione_categorie import (
    recupera_categorie
)
app = FastAPI()

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class SpesaRequest(BaseModel):
    descrizione: str
    categoria: str
    importo: Decimal

    @field_validator("descrizione", "categoria")
    @classmethod
    def valida_testo(cls, valore):
        valore = valore.strip()

        if valore == "":
            raise ValueError(
                "descrizione_o_categoria_vuota",
                "La descrizione e la categoria non possono essere vuote"
            )

        return valore

    @field_validator("importo")
    @classmethod
    def valida_importo(cls, valore):
        if valore < 0:
            raise ValueError(
                "importo_negativo",
                "L'importo non può essere negativo"
            )

        return valore

class OperazioneResponse(BaseModel):
    message: str
    id: int

class SpesaResponseData(BaseModel):
    id: int
    descrizione: str
    categoria: str
    importo: float

class CategoriaResponseData(BaseModel):
    id: int
    nome: str
@app.get("/")
def read_root():
    """Restituisce un messaggio informativo sull'API."""
    return {"message": "Expense Tracker API"}

#SPESE

@app.get("/spese", response_model=list[SpesaResponseData])
def recupero_spese_api():
    spese = recupera_spese()
    return [
            {
                "id": spesa.id,
                "descrizione": spesa.descrizione,
                "categoria": spesa.categoria.nome,
                "importo": spesa.importo
            }
            for spesa in spese
        ]

@app.post("/spese", status_code=201, response_model=OperazioneResponse)
def aggiungi_spesa_api(spesa: SpesaRequest):
    nuova_spesa = aggiungi_spesa(spesa.descrizione, spesa.categoria, spesa.importo)
    return {
        "message": "Spesa aggiunta con successo",
        "id": nuova_spesa.id
    }

@app.delete("/spese/{id_spesa}", response_model=OperazioneResponse)
def elimina_spesa_api(id_spesa: int):
    try:
        elimina_spesa(id_spesa)
    except SpesaNonTrovataError:
        raise HTTPException(
            status_code=404,
            detail="La spesa con l'id indicato non esiste",
        )

    return {
        "message": "Spesa rimossa",
        "id": id_spesa
    }



@app.get("/spese/{id_spesa}", response_model=SpesaResponseData)
def recupera_spesa_api(id_spesa: int):
    try:
        spesa = recupera_spesa(id_spesa)
    except SpesaNonTrovataError:
        raise HTTPException(
            status_code=404,
            detail="La spesa non esiste"
        )
    return {
        "id": id_spesa,
        "descrizione": spesa.descrizione,
        "categoria": spesa.categoria.nome,
        "importo": spesa.importo,
    }
@app.put("/spese/{id_spesa}", response_model=SpesaResponseData)
def modifica_spesa_api(id_spesa: int, spesa: SpesaRequest):
    try:
        spesa_aggiornata = modifica_spesa(
            id_spesa,
            spesa.descrizione,
            spesa.categoria,
            spesa.importo,

        )
    except SpesaNonTrovataError:
        raise HTTPException(
            status_code=404,
            detail = "La spesa non esiste"
        )
    return {
        "id": spesa_aggiornata.id,
        "descrizione": spesa_aggiornata.descrizione,
        "categoria": spesa_aggiornata.categoria.nome,
        "importo": spesa_aggiornata.importo
    }

# CATEGORIE

@app.get("/categorie", response_model=list[CategoriaResponseData])
def recupero_categorie_api():
    categorie = recupera_categorie()
    return [
        {
            "id": categoria.id,
            "nome": categoria.nome
        }
        for categoria in categorie
    ]
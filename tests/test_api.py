from datetime import date
from decimal import Decimal

import pytest

import api
from api import app
from fastapi.testclient import TestClient

@pytest.fixture
def client(database_test):
    with TestClient(app) as client:
        yield client

def test_lista_spese_vuota(client):
    risposta = client.get("/spese")

    assert risposta.status_code == 200
    assert risposta.json() == []

def test_aggiungi_spesa(client):
    risposta = client.post("/spese", json={"descrizione": "Pizza", "categoria": "cibo", "importo": 12.50, "data": date.today().isoformat()})

    assert risposta.status_code == 201

    dati = risposta.json()

    assert dati["message"] == "Spesa aggiunta con successo"
    id_spesa = dati["id"]
    assert isinstance(id_spesa, int)

    risposta_get = client.get(f"/spese/{id_spesa}")
    assert risposta_get.status_code == 200

    dati_spesa = risposta_get.json()

    assert dati_spesa["descrizione"] == "Pizza"
    assert dati_spesa["id"] == id_spesa
    assert dati_spesa["data"] == date.today().isoformat()

@pytest.mark.parametrize(
    "payload, messaggio_atteso",
    [
        ({"descrizione": "Pizza", "categoria": "cibo", "importo": -10, "data":date.today().isoformat()},"L'importo non può essere negativo"),
        ({"descrizione": "Pizza", "categoria": "     ", "importo": 10, "data":date.today().isoformat()}, "La descrizione e la categoria non possono essere vuote"),
        ({"descrizione": "     ", "categoria": "cibo", "importo": 10, "data":date.today().isoformat()}, "La descrizione e la categoria non possono essere vuote")
    ]
)
def test_aggiungi_spesa_non_valido(client, payload, messaggio_atteso):
    risposta = client.post("/spese", json=payload)
    assert risposta.status_code == 422

    dati = risposta.json()
    assert messaggio_atteso in dati["detail"][0]["msg"]

def test_recupero_spesa_tramite_id(client):
    risposta_post = client.post("/spese",     json={
        "descrizione": "Pizza",
        "categoria": "Cibo",
        "importo": 12.50,
        "data": date.today().isoformat()
    })
    id_spesa = risposta_post.json()["id"]

    risposta = client.get(f"/spese/{id_spesa}")
    assert risposta.status_code == 200
    assert risposta.json() == {
        "id": id_spesa,
        "descrizione": "Pizza",
        "categoria": "Cibo",
        "importo": 12.50,
        "data": date.today().isoformat()
    }

def test_recupero_spesa_tramite_id_non_valido(client):
    risposta = client.get("/spese/99")
    assert risposta.status_code == 404
    dati = risposta.json()
    assert dati["detail"] == "La spesa non esiste"

def test_recupero_spesa_tramite_id_stringa(client):
    risposta = client.get("/spese/abc")
    assert risposta.status_code == 422

def test_rimuovi_spesa(client):
    risposta_post = client.post("/spese", json={"descrizione": "Pizza", "categoria": "cibo", "importo": 12.50, "data":date.today().isoformat()})

    id_spesa = risposta_post.json()["id"]
    risposta_rimozione = client.delete(f"/spese/{id_spesa}")

    assert risposta_rimozione.status_code == 200

    dati_risposta_rimozione = risposta_rimozione.json()

    assert dati_risposta_rimozione["message"] == "Spesa rimossa"
    assert dati_risposta_rimozione["id"] == id_spesa

    risposta_get = client.get(f"/spese/{id_spesa}")
    assert risposta_get.status_code == 404

def test_rimuovi_spesa_non_valido(client):
    risposta = client.delete("/spese/99")
    assert risposta.status_code == 404

def test_aggiorna_spesa_esistente(client):
    risposta_post = client.post("/spese", json={"descrizione": "Pizza", "categoria": "cibo", "importo": 12.50, "data":date.today().isoformat()})
    id_spesa = risposta_post.json()["id"]

    risposta_modifica = client.put(f"/spese/{id_spesa}", json={"descrizione": "Panino", "categoria": "Cibo", "importo": 13.50, "data":date.today().isoformat()})

    assert risposta_modifica.status_code == 200

    dati = risposta_modifica.json()

    assert dati["id"] == id_spesa
    assert dati["descrizione"] == "Panino"
    assert dati["categoria"] == "Cibo"
    assert dati["data"] == date.today().isoformat()

    risposta_get = client.get(f"/spese/{id_spesa}")

    assert risposta_get.status_code == 200
    assert risposta_get.json()["descrizione"] == "Panino"
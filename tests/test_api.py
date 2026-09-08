from decimal import Decimal

import pytest

import api
from api import app
from fastapi.testclient import TestClient

@pytest.fixture
def client(tmp_path, monkeypatch):
    percorso_db_tmp = tmp_path / "spese_test.db"

    monkeypatch.setattr(api, "PERCORSO_DATABASE", percorso_db_tmp)

    with TestClient(app) as client:
        yield client

def test_lista_spese_vuota(client):
    risposta = client.get("/spese")

    assert risposta.status_code == 200
    assert risposta.json() == []

def test_aggiungi_spesa(client):
    risposta = client.post("/spese", json={"descrizione": "Pizza", "categoria": "cibo", "importo": 12.50})
    assert risposta.status_code == 201

    dati = risposta.json()

    assert dati["message"] == "Spesa aggiunta con successo"
    assert dati["id"] == 1

    risposta_get = client.get("/spese")
    assert risposta_get.status_code == 200

    dati_spesa = risposta_get.json()

    assert dati_spesa[0]["descrizione"] == "Pizza"
    assert dati_spesa[0]["id"] == 1

@pytest.mark.parametrize(
    "payload, messaggio_atteso",
    [
        ({"descrizione": "Pizza", "categoria": "cibo", "importo": -10},"L'importo non può essere negativo"),
        ({"descrizione": "Pizza", "categoria": "     ", "importo": 10}, "La descrizione e la categoria non possono essere vuote"),
        ({"descrizione": "     ", "categoria": "cibo", "importo": 10}, "La descrizione e la categoria non possono essere vuote")
    ]
)
def test_aggiungi_spesa_non_valido(client, payload, messaggio_atteso):
    risposta = client.post("/spese", json=payload)
    assert risposta.status_code == 422

    dati = risposta.json()
    assert dati["detail"][0]["msg"] == messaggio_atteso

def test_recupero_spesa_tramite_id(client):
    client.post("/spese",     json={
        "descrizione": "Pizza",
        "categoria": "Cibo",
        "importo": 12.50
    })
    risposta = client.get("/spese/1")
    assert risposta.status_code == 200
    assert risposta.json() == {
        "id": 1,
        "descrizione": "Pizza",
        "categoria": "Cibo",
        "importo": 12.50
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
    client.post("/spese", json={"descrizione": "Pizza", "categoria": "cibo", "importo": 12.50})

    risposta_rimozione = client.delete("/spese/1")
    assert risposta_rimozione.status_code == 200

    dati_risposta_rimozione = risposta_rimozione.json()

    assert dati_risposta_rimozione["message"] == "Spesa rimossa"
    assert dati_risposta_rimozione["id"] == 1

    risposta_get = client.get("/spese/1")
    assert risposta_get.status_code == 404

def test_rimuovi_spesa_non_valido(client):
    risposta = client.delete("/spese/99")
    assert risposta.status_code == 404

def test_aggiorna_spesa_esistente(client):
    client.post("/spese", json={"descrizione": "Pizza", "categoria": "cibo", "importo": 12.50})

    risposta_modifica = client.put("/spese/1", json={"descrizione": "Panino", "categoria": "Cibo", "importo": 13.50})

    assert risposta_modifica.status_code == 200

    dati = risposta_modifica.json()

    assert dati["id"] == 1
    assert dati["descrizione"] == "Panino"
    assert dati["categoria"] == "Cibo"

    risposta_get = client.get("/spese/1")

    assert risposta_get.status_code == 200
    assert risposta_get.json()["descrizione"] == "Panino"
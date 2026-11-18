import pytest

from app import app


@pytest.fixture()
def client():
    app.config.update(TESTING=True)
    return app.test_client()


def test_pagina_inicial_vazia(client):
    response = client.get("/")

    assert response.status_code == 200
    assert "Ainda não há listas" in response.get_data(as_text=True)

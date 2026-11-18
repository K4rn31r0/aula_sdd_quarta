import pytest

from app import app


@pytest.fixture()
def client(tmp_path):
    app.config.update(TESTING=True)
    app.config["LISTS_FILE"] = str(tmp_path / "listas.json")
    return app.test_client()


def test_pagina_inicial_vazia(client):
    response = client.get("/")

    assert response.status_code == 200
    assert "Ainda não há listas" in response.get_data(as_text=True)
    assert "Criar primeira lista" in response.get_data(as_text=True)


def test_pessoa_cria_abrir_renomeia_e_exclui_lista(client):
    criacao = client.post("/listas/nova", data={"nome": "  Compras  "})
    assert criacao.status_code == 302

    inicio = client.get("/")
    texto_inicio = inicio.get_data(as_text=True)
    assert "Compras" in texto_inicio

    inicio_id = client.application.config["LIST_MANAGER"].get_all()[0]["id"]
    abertura = client.get(f"/listas/{inicio_id}")
    assert abertura.status_code == 200
    assert "Compras" in abertura.get_data(as_text=True)

    renomeacao = client.post(f"/listas/{inicio_id}/renomear", data={"nome": "Mercado"})
    assert renomeacao.status_code == 302
    assert "Mercado" in client.get(f"/listas/{inicio_id}").get_data(as_text=True)

    confirmacao = client.post(f"/listas/{inicio_id}/excluir")
    assert confirmacao.status_code == 302
    assert "Ainda não há listas" in client.get("/").get_data(as_text=True)


def test_conflito_de_criacao_preserva_dado_digitado(client):
    client.post("/listas/nova", data={"nome": "Compras"})

    response = client.post("/listas/nova", data={"nome": " compras "})

    assert response.status_code == 200
    assert "Já existe uma lista com este nome" in response.get_data(as_text=True)
    assert 'value=" compras "' in response.get_data(as_text=True)


def test_conflito_de_renomeacao_preserva_dado_e_exclusao_exige_confirmacao(client):
    primeira = client.post("/listas/nova", data={"nome": "Compras"})
    segunda = client.post("/listas/nova", data={"nome": "Mercado"})
    manager = client.application.config["LIST_MANAGER"]
    primeira_id = manager.get_by_name("Compras")["id"]

    response = client.post(f"/listas/{primeira_id}/renomear", data={"nome": " mercado "})

    assert response.status_code == 200
    assert "Já existe uma lista com este nome" in response.get_data(as_text=True)
    assert 'value=" mercado "' in response.get_data(as_text=True)

    confirmacao = client.get(f"/listas/{primeira_id}/excluir")
    assert "Deseja excluir" in confirmacao.get_data(as_text=True)

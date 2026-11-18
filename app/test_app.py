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


def test_pessoa_adiciona_edita_marca_desmarca_e_remove_itens(client):
    client.post("/listas/nova", data={"nome": "Compras"})
    manager = client.application.config["LIST_MANAGER"]
    lista_id = manager.get_by_name("Compras")["id"]

    adicionou = client.post(f"/listas/{lista_id}/itens", data={"nome": " Arroz ", "quantidade": " 1 kg "})
    assert adicionou.status_code == 302
    item_id = manager.get_sorted_items(lista_id)[0]["id"]

    pagina = client.get(f"/listas/{lista_id}")
    texto = pagina.get_data(as_text=True)
    assert "Arroz" in texto
    assert "1 kg" in texto
    assert "Nenhum item na lista" not in texto

    marcou = client.post(f"/listas/{lista_id}/itens/{item_id}/comprado", data={"comprado": "true"})
    assert marcou.status_code == 302

    editou = client.post(
        f"/listas/{lista_id}/itens/{item_id}/editar",
        data={"nome": "Arroz integral", "quantidade": "2 kg"},
    )
    assert editou.status_code == 302
    pagina = client.get(f"/listas/{lista_id}")
    texto = pagina.get_data(as_text=True)
    assert "Arroz integral" in texto
    assert "Arroz integral" in texto

    desmarcou = client.post(f"/listas/{lista_id}/itens/{item_id}/comprado", data={"comprado": "false"})
    assert desmarcou.status_code == 302

    removeu = client.post(f"/listas/{lista_id}/itens/{item_id}/remover")
    assert removeu.status_code == 302
    vazia = client.get(f"/listas/{lista_id}")
    assert "Nenhum item na lista" in vazia.get_data(as_text=True)
    assert "Adicionar item" in vazia.get_data(as_text=True)


def test_conflito_de_item_preserva_nome_e_quantidade(client):
    client.post("/listas/nova", data={"nome": "Compras"})
    manager = client.application.config["LIST_MANAGER"]
    lista_id = manager.get_by_name("Compras")["id"]
    client.post(f"/listas/{lista_id}/itens", data={"nome": "Leite", "quantidade": "1 L"})

    response = client.post(f"/listas/{lista_id}/itens", data={"nome": " leite ", "quantidade": "2 L"})

    assert response.status_code == 200
    assert "Já existe um item com este nome" in response.get_data(as_text=True)
    assert 'value=" leite "' in response.get_data(as_text=True)
    assert 'value="2 L"' in response.get_data(as_text=True)

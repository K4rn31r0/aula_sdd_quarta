import json

import pytest

from app.list_manager import ListManager


def test_criar_lista_normaliza_nome_e_persiste(tmp_path):
    arquivo = tmp_path / "listas.json"
    gerenciador = ListManager(arquivo)

    lista = gerenciador.create("  Compras da Semana  ")

    assert lista["name"] == "Compras da Semana"
    assert json.loads(arquivo.read_text(encoding="utf-8"))["lists"][0]["name"] == "Compras da Semana"


@pytest.mark.parametrize("nome", ["", "   ", "x" * 101])
def test_criar_lista_rejeita_nome_vazio_ou_extenso(tmp_path, nome):
    gerenciador = ListManager(tmp_path / "listas.json")

    with pytest.raises(ValueError):
        gerenciador.create(nome)


def test_criar_lista_rejeita_nomes_equivalentes(tmp_path):
    gerenciador = ListManager(tmp_path / "listas.json")
    gerenciador.create("  Compras ")

    with pytest.raises(ValueError, match="Já existe uma lista com este nome"):
        gerenciador.create("compras")


def test_renomear_lista_respeita_unicidade(tmp_path):
    gerenciador = ListManager(tmp_path / "listas.json")
    primeira = gerenciador.create("Compras")
    segunda = gerenciador.create("Mercado")

    with pytest.raises(ValueError, match="Já existe uma lista com este nome"):
        gerenciador.rename(primeira["id"], " mercado ")

    renomeada = gerenciador.rename(primeira["id"], " Casa ")
    assert renomeada["name"] == "Casa"
    assert gerenciador.get(primeira["id"])["name"] == "Casa"
    assert gerenciador.get(segunda["id"])["name"] == "Mercado"


def test_excluir_lista_por_identificacao(tmp_path):
    gerenciador = ListManager(tmp_path / "listas.json")
    lista = gerenciador.create("Compras")

    assert gerenciador.delete(lista["id"]) is True
    assert gerenciador.get(lista["id"]) is None


def test_adicionar_item_normaliza_campos_e_persiste(tmp_path):
    gerenciador = ListManager(tmp_path / "listas.json")
    lista = gerenciador.create("Compras")

    item = gerenciador.add_item(lista["id"], "  Arroz  ", "  2 kg  ")

    assert item["name"] == "Arroz"
    assert item["quantity"] == "2 kg"
    assert item["purchased"] is False
    assert gerenciador.get(lista["id"])["items"][0]["id"] == item["id"]


@pytest.mark.parametrize("nome", ["", "   ", "x" * 101])
def test_adicionar_item_rejeita_nome_vazio_ou_extenso(tmp_path, nome):
    gerenciador = ListManager(tmp_path / "listas.json")
    lista = gerenciador.create("Compras")

    with pytest.raises(ValueError):
        gerenciador.add_item(lista["id"], nome, "")


def test_adicionar_item_rejeita_quantidade_extensa_e_normaliza_espacos(tmp_path):
    gerenciador = ListManager(tmp_path / "listas.json")
    lista = gerenciador.create("Compras")

    with pytest.raises(ValueError, match="máximo 200"):
        gerenciador.add_item(lista["id"], "Feijão", "x" * 201)

    item = gerenciador.add_item(lista["id"], "Feijão", "   ")
    assert item["quantity"] is None


def test_itens_equivalentes_sao_impedidos_e_edicao_respeita_unicidade(tmp_path):
    gerenciador = ListManager(tmp_path / "listas.json")
    lista = gerenciador.create("Compras")
    primeiro = gerenciador.add_item(lista["id"], "Leite", "1 L")

    with pytest.raises(ValueError, match="Já existe um item"):
        gerenciador.add_item(lista["id"], " leite ", "2 L")

    segundo = gerenciador.add_item(lista["id"], "Pão", "")
    with pytest.raises(ValueError, match="Já existe um item"):
        gerenciador.edit_item(lista["id"], segundo["id"], " leite ", "3 L")

    editado = gerenciador.edit_item(lista["id"], primeiro["id"], "  Leite integral  ", " ")
    assert editado["name"] == "Leite integral"
    assert editado["quantity"] is None


def test_editar_marca_desmarca_ordena_e_remove_itens(tmp_path):
    gerenciador = ListManager(tmp_path / "listas.json")
    lista = gerenciador.create("Compras")
    arroz = gerenciador.add_item(lista["id"], "Arroz", "1 kg")
    feijao = gerenciador.add_item(lista["id"], "Feijão", None)

    gerenciador.set_item_purchased(lista["id"], arroz["id"], True)
    editado = gerenciador.edit_item(lista["id"], arroz["id"], "Arroz branco", "2 kg")

    assert editado["purchased"] is True
    assert [item["name"] for item in gerenciador.get_sorted_items(lista["id"])] == ["Feijão", "Arroz branco"]

    gerenciador.set_item_purchased(lista["id"], arroz["id"], False)
    assert [item["name"] for item in gerenciador.get_sorted_items(lista["id"])] == ["Arroz branco", "Feijão"]

    assert gerenciador.remove_item(lista["id"], feijao["id"]) is True
    assert gerenciador.get_sorted_items(lista["id"])[0]["name"] == "Arroz branco"


def test_copiar_lista_mantem_itens_reinicia_compra_e_preserva_original(tmp_path):
    gerenciador = ListManager(tmp_path / "listas.json")
    original = gerenciador.create("Compras")
    gerenciador.add_item(original["id"], "Arroz", "1 kg")
    gerenciador.add_item(original["id"], "Feijão", None)
    arroz = gerenciador.get_items(original["id"])[0]
    gerenciador.set_item_purchased(original["id"], arroz["id"], True)

    copia = gerenciador.copy(original["id"])

    assert copia["name"] == "Compras (cópia)"
    assert [item["name"] for item in gerenciador.get_items(copia["id"])] == ["Arroz", "Feijão"]
    assert all(not item["purchased"] for item in gerenciador.get_items(copia["id"]))
    assert gerenciador.get_items(original["id"])[0]["purchased"] is True
    assert gerenciador.get(original["id"])["name"] == "Compras"


def test_copiar_lista_usa_nomes_sequenciais_disponiveis(tmp_path):
    gerenciador = ListManager(tmp_path / "listas.json")
    original = gerenciador.create("Compras")

    primeira = gerenciador.copy(original["id"])
    segunda = gerenciador.copy(original["id"])
    terceira = gerenciador.copy(original["id"])

    assert [primeira["name"], segunda["name"], terceira["name"]] == [
        "Compras (cópia)",
        "Compras (cópia 2)",
        "Compras (cópia 3)",
    ]


def test_reutilizar_lista_desmarca_itens_sem_alterar_itens(tmp_path):
    gerenciador = ListManager(tmp_path / "listas.json")
    lista = gerenciador.create("Compras")
    arroz = gerenciador.add_item(lista["id"], "Arroz", "1 kg")
    feijao = gerenciador.add_item(lista["id"], "Feijão", None)
    gerenciador.set_item_purchased(lista["id"], arroz["id"], True)

    reutilizada = gerenciador.reuse(lista["id"])

    assert reutilizada["name"] == "Compras"
    assert gerenciador.get_items(lista["id"]) == [
        {"id": arroz["id"], "name": "Arroz", "quantity": "1 kg", "purchased": False},
        {"id": feijao["id"], "name": "Feijão", "quantity": None, "purchased": False},
    ]


def test_limpar_comprados_remove_somente_itens_marcados(tmp_path):
    gerenciador = ListManager(tmp_path / "listas.json")
    lista = gerenciador.create("Compras")
    arroz = gerenciador.add_item(lista["id"], "Arroz", "1 kg")
    feijao = gerenciador.add_item(lista["id"], "Feijão", None)
    gerenciador.set_item_purchased(lista["id"], arroz["id"], True)

    limpa = gerenciador.clear_purchased(lista["id"])

    assert limpa["name"] == "Compras"
    assert gerenciador.get_items(lista["id"]) == [
        {"id": feijao["id"], "name": "Feijão", "quantity": None, "purchased": False}
    ]


def test_operacoes_sobre_lista_inexistente_nao_criam_ou_corrompem_dados(tmp_path):
    arquivo = tmp_path / "listas.json"
    gerenciador = ListManager(arquivo)
    gerenciador.create("Compras")
    antes = json.loads(arquivo.read_text(encoding="utf-8"))

    assert gerenciador.copy("inexistente") is None
    assert gerenciador.reuse("inexistente") is None
    assert gerenciador.clear_purchased("inexistente") is None
    assert json.loads(arquivo.read_text(encoding="utf-8")) == antes

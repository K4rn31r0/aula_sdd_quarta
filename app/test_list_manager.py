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

import json
import uuid
from pathlib import Path


DATA_FILE = Path(__file__).with_name("listas.json")


def normalize_name(name):
    if name is None:
        return ""
    return str(name).strip()


def validate_name(name):
    normalized = normalize_name(name)
    if not normalized:
        raise ValueError("O nome da lista é obrigatório.")
    if len(normalized) > 100:
        raise ValueError("O nome da lista deve ter no máximo 100 caracteres.")
    return normalized


class ListManager:
    def __init__(self, data_file=None):
        self.data_file = Path(data_file or DATA_FILE)

    def _read(self):
        if not self.data_file.exists():
            return {"lists": []}
        with self.data_file.open("r", encoding="utf-8") as archive:
            data = json.load(archive)
        return data if isinstance(data, dict) else {"lists": []}

    def _write(self, data):
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        with self.data_file.open("w", encoding="utf-8") as archive:
            json.dump(data, archive, ensure_ascii=False, indent=2)

    def create(self, name):
        name = validate_name(name)
        data = self._read()
        if self._find_by_normalized_name(data, name) is not None:
            raise ValueError("Já existe uma lista com este nome.")
        lista = {"id": str(uuid.uuid4()), "name": name}
        data.setdefault("lists", []).append(lista)
        self._write(data)
        return lista

    def _find_by_normalized_name(self, data, name):
        wanted = normalize_name(name).casefold()
        for lista in data.setdefault("lists", []):
            if normalize_name(lista.get("name")).casefold() == wanted:
                return lista
        return None

    def get_all(self):
        return self._read().get("lists", [])

    def get(self, list_id):
        for lista in self.get_all():
            if lista["id"] == str(list_id):
                return lista
        return None

    def get_by_name(self, name):
        return self._find_by_normalized_name(self._read(), normalize_name(name))

    def rename(self, list_id, name):
        name = validate_name(name)
        data = self._read()
        existente = self._find_by_normalized_name(data, name)
        if existente is not None and existente["id"] != str(list_id):
            raise ValueError("Já existe uma lista com este nome.")
        for lista in data.setdefault("lists", []):
            if lista["id"] == str(list_id):
                lista["name"] = name
                self._write(data)
                return lista
        return None

    def delete(self, list_id):
        data = self._read()
        lists = data.setdefault("lists", [])
        remaining = [lista for lista in lists if lista["id"] != str(list_id)]
        if len(remaining) == len(lists):
            return False
        data["lists"] = remaining
        self._write(data)
        return True

    create_list = create
    rename_list = rename
    delete_list = delete
    open_list = get
    list_all = get_all


def create_list(name, data_file=None):
    return ListManager(data_file).create(name)


def rename_list(list_id, name, data_file=None):
    return ListManager(data_file).rename(list_id, name)


def delete_list(list_id, data_file=None):
    return ListManager(data_file).delete(list_id)


def open_list(list_id, data_file=None):
    return ListManager(data_file).get(list_id)

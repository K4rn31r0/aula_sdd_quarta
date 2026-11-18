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


def normalize_quantity(quantity):
    if quantity is None:
        return None
    normalized = str(quantity).strip()
    return normalized or None


def validate_item_name(name):
    normalized = normalize_name(name)
    if not normalized:
        raise ValueError("O nome do item é obrigatório.")
    if len(normalized) > 100:
        raise ValueError("O nome do item deve ter no máximo 100 caracteres.")
    return normalized


def validate_quantity(quantity):
    normalized = normalize_quantity(quantity)
    if normalized is not None and len(normalized) > 200:
        raise ValueError("A quantidade deve ter no máximo 200 caracteres.")
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

    def add_item(self, list_id, name, quantity=None):
        name = validate_item_name(name)
        quantity = validate_quantity(quantity)
        data = self._read()
        for lista in data.setdefault("lists", []):
            if lista["id"] == str(list_id):
                items = lista.setdefault("items", [])
                wanted = name.casefold()
                if any(normalize_name(item.get("name")).casefold() == wanted for item in items):
                    raise ValueError("Já existe um item com este nome na lista.")
                item = {
                    "id": str(uuid.uuid4()),
                    "name": name,
                    "quantity": quantity,
                    "purchased": False,
                }
                items.append(item)
                self._write(data)
                return item
        return None

    def edit_item(self, list_id, item_id, name, quantity=None):
        name = validate_item_name(name)
        quantity = validate_quantity(quantity)
        data = self._read()
        for lista in data.setdefault("lists", []):
            if lista["id"] != str(list_id):
                continue
            items = lista.setdefault("items", [])
            wanted = name.casefold()
            if any(
                item["id"] != str(item_id)
                and normalize_name(item.get("name")).casefold() == wanted
                for item in items
            ):
                raise ValueError("Já existe um item com este nome na lista.")
            for item in items:
                if item["id"] == str(item_id):
                    item["name"] = name
                    item["quantity"] = quantity
                    self._write(data)
                    return item
        return None

    def set_item_purchased(self, list_id, item_id, purchased):
        if isinstance(purchased, str):
            purchased = purchased.strip().casefold() in ("true", "1", "sim", "on")
        data = self._read()
        for lista in data.setdefault("lists", []):
            if lista["id"] == str(list_id):
                for item in lista.setdefault("items", []):
                    if item["id"] == str(item_id):
                        item["purchased"] = bool(purchased)
                        self._write(data)
                        return item
        return None

    def toggle_item(self, list_id, item_id):
        data = self._read()
        for lista in data.setdefault("lists", []):
            if lista["id"] == str(list_id):
                for item in lista.setdefault("items", []):
                    if item["id"] == str(item_id):
                        item["purchased"] = not item.get("purchased", False)
                        self._write(data)
                        return item
        return None

    def unmark_item_purchased(self, list_id, item_id):
        return self.set_item_purchased(list_id, item_id, False)

    def remove_item(self, list_id, item_id):
        data = self._read()
        for lista in data.setdefault("lists", []):
            if lista["id"] == str(list_id):
                items = lista.setdefault("items", [])
                remaining = [item for item in items if item["id"] != str(item_id)]
                if len(remaining) == len(items):
                    return False
                lista["items"] = remaining
                self._write(data)
                return True
        return False

    def get_items(self, list_id):
        lista = self.get(list_id)
        return lista.get("items", []) if lista is not None else []

    def get_sorted_items(self, list_id):
        items = self.get_items(list_id)
        return [item for item in items if not item.get("purchased", False)] + [
            item for item in items if item.get("purchased", False)
        ]

    def copy(self, list_id):
        data = self._read()
        origem = next(
            (lista for lista in data.setdefault("lists", []) if lista["id"] == str(list_id)),
            None,
        )
        if origem is None:
            return None

        base = f"{origem['name']} (cópia)"
        name = base
        numero = 2
        while self._find_by_normalized_name(data, name) is not None:
            name = f"{origem['name']} (cópia {numero})"
            numero += 1

        copied_items = [
            {
                "id": str(uuid.uuid4()),
                "name": item["name"],
                "quantity": item.get("quantity"),
                "purchased": False,
            }
            for item in origem.get("items", [])
        ]
        copia = {"id": str(uuid.uuid4()), "name": name, "items": copied_items}
        data["lists"].append(copia)
        self._write(data)
        return copia

    def reuse(self, list_id):
        data = self._read()
        for lista in data.setdefault("lists", []):
            if lista["id"] == str(list_id):
                for item in lista.setdefault("items", []):
                    item["purchased"] = False
                self._write(data)
                return lista
        return None

    def clear_purchased(self, list_id):
        data = self._read()
        for lista in data.setdefault("lists", []):
            if lista["id"] == str(list_id):
                lista["items"] = [
                    item
                    for item in lista.setdefault("items", [])
                    if not item.get("purchased", False)
                ]
                self._write(data)
                return lista
        return None

    create_item = add_item
    update_item = edit_item
    mark_item_purchased = set_item_purchased
    delete_item = remove_item
    toggle_item_purchased = toggle_item

    create_list = create
    rename_list = rename
    delete_list = delete
    open_list = get
    list_all = get_all
    copy_list = copy
    reuse_list = reuse
    clear_purchased_items = clear_purchased


def create_list(name, data_file=None):
    return ListManager(data_file).create(name)


def rename_list(list_id, name, data_file=None):
    return ListManager(data_file).rename(list_id, name)


def delete_list(list_id, data_file=None):
    return ListManager(data_file).delete(list_id)


def open_list(list_id, data_file=None):
    return ListManager(data_file).get(list_id)


def copy_list(list_id, data_file=None):
    return ListManager(data_file).copy(list_id)


def reuse_list(list_id, data_file=None):
    return ListManager(data_file).reuse(list_id)


def clear_purchased_items(list_id, data_file=None):
    return ListManager(data_file).clear_purchased(list_id)

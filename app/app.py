from flask import Flask, redirect, render_template, request, url_for

from .list_manager import DATA_FILE, ListManager


app = Flask(__name__)
app.config["LISTS_FILE"] = None


def get_manager():
    manager = app.config.get("LIST_MANAGER")
    data_file = app.config.get("LISTS_FILE")
    expected_file = str(data_file or DATA_FILE)
    if manager is None or str(getattr(manager, "data_file", "")) != expected_file:
        manager = ListManager(data_file)
        app.config["LIST_MANAGER"] = manager
    return manager


@app.route("/")
def index():
    return render_template("index.html", listas=get_manager().get_all())


@app.route("/listas/nova", methods=["GET", "POST"])
def nova_lista():
    raw_name = request.form.get("nome", request.form.get("name", "")) if request.method == "POST" else ""
    error = None
    if request.method == "POST":
        try:
            get_manager().create(raw_name)
            return redirect(url_for("index"))
        except ValueError as exc:
            error = str(exc)
    return render_template("index.html", listas=get_manager().get_all(), form_name=raw_name, error=error)


@app.route("/listas", methods=["POST"])
def criar_lista():
    return nova_lista()


@app.route("/listas/<list_id>")
def abrir_lista(list_id):
    lista = get_manager().get(list_id)
    if lista is None:
        return redirect(url_for("index"))
    return render_template(
        "index.html",
        listas=get_manager().get_all(),
        lista=lista,
        itens=get_manager().get_sorted_items(list_id),
    )


@app.route("/listas/<list_id>/renomear", methods=["GET", "POST"])
def renomear_lista(list_id):
    lista = get_manager().get(list_id)
    if lista is None:
        return redirect(url_for("index"))
    raw_name = request.form.get("nome", request.form.get("name", "")) if request.method == "POST" else lista["name"]
    error = None
    if request.method == "POST":
        try:
            lista = get_manager().rename(list_id, raw_name)
            return redirect(url_for("abrir_lista", list_id=list_id))
        except ValueError as exc:
            error = str(exc)
    return render_template("index.html", listas=get_manager().get_all(), lista=lista, form_name=raw_name, error=error)


@app.route("/listas/<list_id>/excluir", methods=["GET", "POST"])
def excluir_lista(list_id):
    lista = get_manager().get(list_id)
    if lista is None:
        return redirect(url_for("index"))
    if request.method == "POST":
        get_manager().delete(list_id)
        return redirect(url_for("index"))
    return render_template("index.html", listas=get_manager().get_all(), lista=lista, confirmar_exclusao=True)


@app.route("/listas/<list_id>/copiar", methods=["POST"])
def copiar_lista(list_id):
    copia = get_manager().copy(list_id)
    if copia is None:
        return redirect(url_for("index"))
    return redirect(url_for("abrir_lista", list_id=copia["id"]))


@app.route("/listas/<list_id>/reutilizar", methods=["GET", "POST"])
def reutilizar_lista(list_id):
    lista = get_manager().get(list_id)
    if lista is None:
        return redirect(url_for("index"))
    if request.method == "POST":
        get_manager().reuse(list_id)
        return redirect(url_for("abrir_lista", list_id=list_id))
    return render_template(
        "index.html",
        listas=get_manager().get_all(),
        lista=lista,
        confirmar_reutilizacao=True,
    )


@app.route("/listas/<list_id>/limpar-comprados", methods=["GET", "POST"])
def limpar_comprados(list_id):
    lista = get_manager().get(list_id)
    if lista is None:
        return redirect(url_for("index"))
    if request.method == "POST":
        get_manager().clear_purchased(list_id)
        return redirect(url_for("abrir_lista", list_id=list_id))
    return render_template(
        "index.html",
        listas=get_manager().get_all(),
        lista=lista,
        confirmar_limpeza=True,
    )


@app.route("/listas/<list_id>/itens", methods=["POST"])
@app.route("/listas/<list_id>/itens/nova", methods=["POST"])
@app.route("/listas/<list_id>/itens/adicionar", methods=["POST"])
def adicionar_item(list_id):
    lista = get_manager().get(list_id)
    if lista is None:
        return redirect(url_for("index"))
    raw_name = request.form.get("nome", request.form.get("name", ""))
    raw_quantity = request.form.get("quantidade", request.form.get("quantity", ""))
    try:
        get_manager().add_item(list_id, raw_name, raw_quantity)
        return redirect(url_for("abrir_lista", list_id=list_id))
    except ValueError as exc:
        return render_template(
            "index.html",
            listas=get_manager().get_all(),
            lista=lista,
            itens=get_manager().get_sorted_items(list_id),
            error=str(exc),
            item_form_name=raw_name,
            item_form_quantity=raw_quantity,
        )


@app.route("/listas/<list_id>/itens/<item_id>/editar", methods=["GET", "POST"])
def editar_item(list_id, item_id):
    lista = get_manager().get(list_id)
    if lista is None:
        return redirect(url_for("index"))
    item = next((item for item in lista.get("items", []) if item["id"] == str(item_id)), None)
    if item is None:
        return redirect(url_for("abrir_lista", list_id=list_id))

    raw_name = request.form.get("nome", request.form.get("name", "")) if request.method == "POST" else item["name"]
    raw_quantity = (
        request.form.get("quantidade", request.form.get("quantity", ""))
        if request.method == "POST"
        else (item.get("quantity") or "")
    )
    error = None
    if request.method == "POST":
        try:
            get_manager().edit_item(list_id, item_id, raw_name, raw_quantity)
            return redirect(url_for("abrir_lista", list_id=list_id))
        except ValueError as exc:
            error = str(exc)
    return render_template(
        "index.html",
        listas=get_manager().get_all(),
        lista=lista,
        itens=get_manager().get_sorted_items(list_id),
        error=error,
        edit_item_id=item_id,
        item_form_name=raw_name,
        item_form_quantity=raw_quantity,
    )


@app.route("/listas/<list_id>/itens/<item_id>/comprado", methods=["POST"])
@app.route("/listas/<list_id>/itens/<item_id>/marcar", methods=["POST"])
@app.route("/listas/<list_id>/itens/<item_id>/desmarcar", methods=["POST"])
def marcar_item(list_id, item_id):
    raw = request.form.get("comprado", request.form.get("purchased", ""))
    if not raw and request.path.endswith("/marcar"):
        purchased = True
    elif not raw and request.path.endswith("/desmarcar"):
        purchased = False
    else:
        purchased = str(raw).lower() in ("true", "1", "sim", "on")
    get_manager().set_item_purchased(list_id, item_id, purchased)
    return redirect(url_for("abrir_lista", list_id=list_id))


@app.route("/listas/<list_id>/itens/<item_id>/alternar", methods=["POST"])
def alternar_item(list_id, item_id):
    get_manager().toggle_item(list_id, item_id)
    return redirect(url_for("abrir_lista", list_id=list_id))


@app.route("/listas/<list_id>/itens/<item_id>/remover", methods=["POST"])
def remover_item(list_id, item_id):
    get_manager().remove_item(list_id, item_id)
    return redirect(url_for("abrir_lista", list_id=list_id))


if __name__ == "__main__":
    app.run(debug=True)

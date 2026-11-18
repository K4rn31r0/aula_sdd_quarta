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
    return render_template("index.html", listas=get_manager().get_all(), lista=lista)


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


if __name__ == "__main__":
    app.run(debug=True)


import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def conectar_banco():
    conexao = sqlite3.connect("produtos.db")
    conexao.row_factory = sqlite3.Row
    return conexao

def criar_banco():
    with conectar_banco() as conexao:
        conexao.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                preco REAL NOT NULL,
                quantidade INTEGER NOT NULL,
                categoria TEXT NOT NULL
            )
        """)


@app.route("/")
def inicio():
    pesquisa = request.args.get("pesquisa", "").strip()

    with conectar_banco() as conexao:
        if pesquisa:
            produtos = conexao.execute(
                """SELECT * FROM produtos
                   WHERE nome LIKE ?
                   ORDER BY id DESC""",
                (f"%{pesquisa}%",)
            ).fetchall()
        else:
            produtos = conexao.execute(
                "SELECT * FROM produtos ORDER BY id DESC"
            ).fetchall()

    return render_template(
        "index.html",
        produtos=produtos,
        pesquisa=pesquisa
    )



@app.route("/cadastrar", methods=["POST"])
def cadastrar():
    nome = request.form["nome"].strip()
    preco = float(request.form["preco"])
    quantidade = int(request.form["quantidade"])
    categoria = request.form["categoria"].strip()

    if not nome or not categoria or preco < 0 or quantidade < 0:
        return "Dados inválidos.", 400

    with conectar_banco() as conexao:
        conexao.execute(
            """INSERT INTO produtos
               (nome, preco, quantidade, categoria)
               VALUES (?, ?, ?, ?)""",
            (nome, preco, quantidade, categoria)
        )

    return redirect(url_for("inicio"))


@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    with conectar_banco() as conexao:
        produto = conexao.execute(
            "SELECT * FROM produtos WHERE id = ?", (id,)
        ).fetchone()

    if produto is None:
        return "Produto não encontrado.", 404

    if request.method == "POST":
        try:
            nome = request.form["nome"].strip()
            preco = float(request.form["preco"])
            quantidade = int(request.form["quantidade"])
            categoria = request.form["categoria"].strip()
        except (KeyError, ValueError):
            return "Dados inválidos.", 400

        if not nome or not categoria or preco < 0 or quantidade < 0:
            return "Dados inválidos.", 400

        with conectar_banco() as conexao:
            conexao.execute(
                """UPDATE produtos
                   SET nome = ?, preco = ?,
                       quantidade = ?, categoria = ?
                   WHERE id = ?""",
                (nome, preco, quantidade, categoria, id)
            )

        return redirect(url_for("inicio"))

    return render_template("editar.html", produto=produto)


@app.route("/excluir/<int:id>", methods=["POST"])
def excluir(id):
    with conectar_banco() as conexao:
        conexao.execute(
            "DELETE FROM produtos WHERE id = ?", (id,)
        )

    return redirect(url_for("inicio"))

if __name__ == "__main__":
    criar_banco()
    app.run(debug=True)

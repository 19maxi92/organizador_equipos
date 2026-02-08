from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB = "equipos.db"

def get_db():
    return sqlite3.connect(DB)

@app.route("/", methods=["GET", "POST"])
def index():
    conn = get_db()
    cur = conn.cursor()

    equipos = cur.execute("SELECT id, nombre FROM equipos").fetchall()

    equipo_id = request.args.get("equipo", equipos[0][0] if equipos else None)

    if request.method == "POST":
        equipo_id = request.form["equipo_id"]

        for key in request.form:
            if key.startswith("estado_"):
                puerto = key.split("_")[1]
                estado = request.form[key]
                comentario = request.form.get(f"comentario_{puerto}", "")

                cur.execute("""
                    UPDATE puertos
                    SET estado = ?, comentario = ?
                    WHERE equipo_id = ? AND puerto = ?
                """, (estado, comentario, equipo_id, puerto))

        conn.commit()
        return redirect(url_for("index", equipo=equipo_id))

    puertos = cur.execute("""
        SELECT puerto, estado, comentario
        FROM puertos
        WHERE equipo_id = ?
        ORDER BY puerto
    """, (equipo_id,)).fetchall()

    conn.close()

    return render_template(
        "index.html",
        equipos=equipos,
        equipo_id=int(equipo_id),
        puertos=puertos
    )

if __name__ == "__main__":
    app.run(debug=True)

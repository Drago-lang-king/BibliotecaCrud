from flask import Flask, render_template, url_for, redirect, request, flash

import sqlite3

app = Flask(__name__)
app.secret_key = "UnaClaveSegura"

con = sqlite3.connect("Biblioteca.db")
cursor = con.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        apellidos TEXT,
        carnet TEXT UNIQUE
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS libros(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo  TEXT,
        autor  TEXT,
        anio INTEGER
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS prestamos(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha_prestamo TEXT,
    fecha_devolucion TEXT,
    libro_id INTEGER, 
    usuario_id INTEGER,

    FOREIGN KEY (libro_id) REFERENCES libros(id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
    )
""")

con.commit()
con.close()

def get_db_connection():
    con = sqlite3.connect("Biblioteca.db")
    con.row_factory = sqlite3.Row
    return con 

@app.route("/")
def index():
    return redirect(url_for("usuarios"))

@app.route("/libros")
def libros():
    con = get_db_connection()
    libros = con.execute('SELECT * FROM libros').fetchall()
    con.close()
    return render_template('libros.html', libros=libros)

@app.route("/nuevo/libro", methods=['GET','POST'])
def nuevo_libro():
    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        anio = request.form['anio']

        con = get_db_connection()
        con.execute("INSERT INTO libros (titulo, autor, anio) VALUES(?,?,?)",(titulo, autor, anio))

        con.commit()
        con.close()

        flash('Libro agregado Correctamente')
        return redirect(url_for('libros'))
    return render_template('libro_form.html')

@app.route("/libro/editar/<int:id>", methods=['GET','POST'])
def editar_libro(id):
    con = get_db_connection()
    cursor = con.execute("SELECT * FROM libros WHERE id = ?",(id,)).fetchone()

    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        anio = request.form['anio']

        con.execute("UPDATE libros SET titulo = ?, autor = ?, anio = ? WHERE id = ?", (titulo, autor, anio, id))

        con.commit()
        con.close()
        flash('Libro Actualizado', 'success')
        return redirect(url_for('libros'))



    return render_template('libro_form.html',cursor=cursor)

@app.route('/libro/eliminar/<int:id>')
def eliminar_libro(id):
    con = get_db_connection()
    con.execute("DELETE FROM libros WHERE id=?",(id,))
    con.commit()
    con.close()
    flash('Libro Eliminado','success')
    return redirect(url_for('libros'))

@app.route("/usuarios")
def usuarios():
    con = get_db_connection()
    usuarios = con.execute('SELECT * FROM usuarios').fetchall()

    con.close()
    return render_template('usuarios.html', usuarios=usuarios)

@app.route('/prestamos')
def prestamos():
    con = get_db_connection()

    prestamos = con.execute("""
        SELECT 
        p.id,
        u.nombre ||' '|| u.apellidos as usuarios,
        p.fecha_prestamo,
        p.fecha_devolucion,
        l.titulo
        FROM libros l
        JOIN prestamos p on l.id = p.libro_id
        JOIN usuarios u on p.usuario_id = u.id
    """).fetchall()

    con.close()
    return render_template('prestamos.html', prestamos=prestamos)

if __name__ == "__main__":
    app.run(debug=True)



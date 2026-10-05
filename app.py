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

print("Base de datos Creada corectamente")

if __name__ == "__main__":
    app.run(debug=True)



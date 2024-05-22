from flask import Flask, render_template, jsonify
import sqlite3

app = Flask(__name__)

# Conexión a la base de datos
def conectar_db():
    conexion = sqlite3.connect('base_de_datos')
    conexion.row_factory = sqlite3.Row
    return conexion

# Ruta para la página principal
@app.route('/')
def index():
    return render_template('dev.html')

# Ruta para obtener libros en formato JSON
@app.route('/api/books')
def obtener_libros():
    conexion = conectar_db()
    cursor = conexion.execute('SELECT * FROM books')
    libros = [dict(row) for row in cursor.fetchall()]
    conexion.close()
    return jsonify(libros)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3

app = Flask(__name__)

# Función para conectar a la base de datos
def conectar_db():
    conexion = sqlite3.connect('base_de_datos')
    conexion.row_factory = sqlite3.Row
    return conexion

# Ruta para la página principal
@app.route('/')
def index():
    return render_template('pagina.html')

# Ruta para la página de libros
@app.route('/libros')
def libros():
    return render_template('libros.html')

# Ruta para obtener libros en formato JSON
@app.route('/api/books')
def obtener_libros():
    conexion = conectar_db()
    cursor = conexion.execute('SELECT * FROM books')
    libros = [dict(row) for row in cursor.fetchall()]
    conexion.close()
    return jsonify(libros)

# Función para obtener autores y sus libros de la base de datos
@app.route('/api/authors', methods=['GET'])
def obtener_autores_con_libros():
    conexion = conectar_db()
    cursor = conexion.execute('''
        SELECT author AS autor_nombre, title AS titulo_libro
        FROM books
        ORDER BY author
    ''')
    autores_con_libros = {}
    for row in cursor.fetchall():
        autor_nombre = row['autor_nombre']
        if autor_nombre not in autores_con_libros:
            autores_con_libros[autor_nombre] = {
                'nombre': autor_nombre,
                'libros': []
            }
        autores_con_libros[autor_nombre]['libros'].append(row['titulo_libro'])
    conexion.close()
    return jsonify(list(autores_con_libros.values()))

# Nueva ruta para mostrar autores
@app.route('/autores')
def mostrar_autores():
    autores = obtener_autores_con_libros()
    return render_template('autores.html', autores=autores)

@app.route('/buscar')
def buscar():
    query = request.args.get('query')
    if not query:
        return jsonify({'error': 'Ingrese un término de búsqueda válido'})

    conexion = conectar_db()
    cursor = conexion.execute('''
        SELECT *
        FROM books
        WHERE title LIKE ? OR author LIKE ?
    ''', ('%' + query + '%', '%' + query + '%'))
    libros = [dict(row) for row in cursor.fetchall()]
    conexion.close()

    if not libros:
        return render_template('busqueda.html', libros=[], message='No se encontraron resultados para la búsqueda')

    return render_template('busqueda.html', libros=libros)

@app.route('/libro/<int:id>')
def mostrar_libro(id):
    conexion = conectar_db()
    cursor = conexion.execute('SELECT * FROM books WHERE id = ?', (id,))
    libro = cursor.fetchone()
    conexion.close()
    if libro:
        return render_template('libro_detalle.html', libro=libro)
    else:
        return "Libro no encontrado", 404

@app.route('/libros/<isbn>')
def obtener_detalles_libro(isbn):
    conexion = conectar_db()
    cursor = conexion.execute('''
        SELECT * FROM books
        WHERE isbn = ?
    ''', (isbn,))
    libro = cursor.fetchone()
    conexion.close()

    if not libro:
        return "Libro no encontrado", 404

    return render_template('detalle_libro.html', libro=libro)

if __name__ == '__main__':
    app.run(debug=True)


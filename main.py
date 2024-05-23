import funciones

# Buscar libros por categorías y guardarlos en la base de datos
categorias = ["Science & Technology", "Science Fiction & Fantasy", "Mystery & Suspense"]

for categoria in categorias:
    libros = funciones.buscar_por_categoria(categoria, 100)
    status, error = funciones.create_book_database(libros)
    if status:
        print(f"Libros de la categoría '{categoria}' guardados correctamente.")
    else:
        print(f"Los libros de la categoría '{categoria}' no se pudieron guardar: {error}")










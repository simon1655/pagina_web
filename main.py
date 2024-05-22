import funciones

categoria_1 = funciones.buscar_por_categoria("Science & Technology", 100)
status, error = funciones.create_book_database(categoria_1)
if status:
    print("Libros guardados correctamente.")
else:
    print("Los libros no se pudieron guardar: ", error)

categoria_2 = funciones.buscar_por_categoria("Science Fiction & Fantasy", 100)
status, error = funciones.create_book_database(categoria_2)
if status:
    print("Libros guardados correctamente.")
else:
    print("Los libros no se pudieron guardar: ", error)

categoria_3 = funciones.buscar_por_categoria("Mystery & Suspense", 100)
status, error = funciones.create_book_database(categoria_3)
if status:
    print("Libros guardados correctamente.")
else:
    print("Los libros no se pudieron guardar: ", error)








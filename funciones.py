import requests
import sqlite3
from typing import Union
def buscar_por_categoria(category: str, results_per_page: int) -> dict:

    url = "https://book-finder1.p.rapidapi.com/api/search"

    querystring = {
        "categories": category,
        "lexile_min": "600",
        "lexile_max": "800",
        "results_per_page": results_per_page,
        "page": "1"
    }

    headers = {
        "X-RapidAPI-Key": "fbc615dc91mshe3a023dccd77a48p1e2f6cjsn2e2ef44125c6",
        "X-RapidAPI-Host": "book-finder1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()

    if "results" not in data:
        return {"error": "No results found"}

    books = {}

    for result in data["results"]:
        title = result["title"]
        author = result["authors"][0] if result["authors"] else "Unknown"
        categories = result["categories"]
        language = result["language"]
        summary = result["summary"]
        isbn = result["recommended_isbns"][0] if result["recommended_isbns"] else "Unknown"
        cover_art_url = result["published_works"][0]["cover_art_url"] if result["published_works"] else "Unknown"

        books[title] = {
            "author": author,
            "categories": categories,
            "language": language,
            "summary": summary,
            "isbn": isbn,
            "cover_art_url": cover_art_url
            
        }
    
    return books

def create_book_database(books: dict) -> Union[bool, str]:
    try:
        # Conexión a la base de datos (se creará si no existe)
        conexion = sqlite3.connect("base_de_datos")
        cursorBF = conexion.cursor()        

        # Crear tabla de libros si no existe
        cursorBF.execute('''CREATE TABLE IF NOT EXISTS books
                    (title TEXT, author TEXT, categories TEXT, language TEXT, summary TEXT, isbn TEXT, cover_art_url TEXT)''')

        # Insertar los datos de los libros en la tabla
        for title, details in books.items():
            cursorBF.execute("INSERT INTO books (title, author, categories, language, summary, isbn, cover_art_url) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (title, details["author"], ", ".join(details["categories"]), details["language"], details["summary"], details["isbn"], details["cover_art_url"]))
    
        # Guardar cambios y cerrar la conexión
        conexion.commit()
        conexion.close()
        return True, ""
    except Exception as e:
        return False, e
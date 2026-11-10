"""Raíz de composición: único lugar donde se conectan puertos con adaptadores."""
from library.application.use_cases import UseCases
from library.infrastructure.persistence.sqlite_book_repository import SqliteBookRepository
from library.infrastructure.web.flask_api import create_app

repository = SqliteBookRepository("library.db")
app = create_app(UseCases.build(repository))

if __name__ == "__main__":
    app.run(port=5000, debug=True)

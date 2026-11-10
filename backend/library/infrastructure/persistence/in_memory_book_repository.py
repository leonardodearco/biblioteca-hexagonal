from typing import Dict, List, Optional

from ...application.ports import BookRepository
from ...domain.book import Book


class InMemoryBookRepository(BookRepository):
    """Adaptador para pruebas: demuestra que la BD es intercambiable."""

    def __init__(self) -> None:
        self._books: Dict[str, Book] = {}

    def save(self, book: Book) -> None:
        self._books[book.id] = book

    def find_by_id(self, book_id: str) -> Optional[Book]:
        return self._books.get(book_id)

    def find_by_isbn(self, isbn: str) -> Optional[Book]:
        return next((b for b in self._books.values() if b.isbn == isbn), None)

    def find_all(self) -> List[Book]:
        return list(self._books.values())

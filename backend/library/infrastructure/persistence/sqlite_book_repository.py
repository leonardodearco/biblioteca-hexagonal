import sqlite3
import threading
from typing import List, Optional

from ...application.ports import BookRepository
from ...domain.book import Book

_SCHEMA = """
CREATE TABLE IF NOT EXISTS books (
    id       TEXT PRIMARY KEY,
    title    TEXT NOT NULL,
    author   TEXT NOT NULL,
    isbn     TEXT NOT NULL UNIQUE,
    borrower TEXT
)
"""


class SqliteBookRepository(BookRepository):
    """Adaptador de salida hacia SQLite (base de datos relacional)."""

    def __init__(self, path: str = "library.db") -> None:
        self._conn = sqlite3.connect(path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._lock = threading.Lock()
        with self._lock:
            self._conn.execute(_SCHEMA)
            self._conn.commit()

    def save(self, book: Book) -> None:
        with self._lock:
            self._conn.execute(
                "INSERT INTO books (id, title, author, isbn, borrower) VALUES (?, ?, ?, ?, ?) "
                "ON CONFLICT(id) DO UPDATE SET title=excluded.title, author=excluded.author, "
                "isbn=excluded.isbn, borrower=excluded.borrower",
                (book.id, book.title, book.author, book.isbn, book.borrower),
            )
            self._conn.commit()

    def find_by_id(self, book_id: str) -> Optional[Book]:
        return self._fetch_one("SELECT * FROM books WHERE id = ?", (book_id,))

    def find_by_isbn(self, isbn: str) -> Optional[Book]:
        return self._fetch_one("SELECT * FROM books WHERE isbn = ?", (isbn,))

    def find_all(self) -> List[Book]:
        with self._lock:
            rows = self._conn.execute("SELECT * FROM books").fetchall()
        return [self._to_entity(row) for row in rows]

    def _fetch_one(self, query: str, params: tuple) -> Optional[Book]:
        with self._lock:
            row = self._conn.execute(query, params).fetchone()
        return self._to_entity(row) if row else None

    @staticmethod
    def _to_entity(row: sqlite3.Row) -> Book:
        return Book(row["id"], row["title"], row["author"], row["isbn"], row["borrower"])

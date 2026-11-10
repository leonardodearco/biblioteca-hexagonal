"""Entidad Book: contiene las reglas de negocio puras."""
from dataclasses import dataclass
from typing import Optional
from uuid import uuid4

from .errors import BookAlreadyLentError, BookNotLentError, InvalidBookError

ISBN_LENGTHS = (10, 13)


def _require_text(value: str, field: str) -> str:
    cleaned = (value or "").strip()
    if not cleaned:
        raise InvalidBookError(f"El campo '{field}' es obligatorio.")
    return cleaned


def _normalize_isbn(raw: str) -> str:
    isbn = _require_text(raw, "isbn").replace("-", "").replace(" ", "")
    if not isbn.isdigit() or len(isbn) not in ISBN_LENGTHS:
        raise InvalidBookError("El ISBN debe tener 10 o 13 dígitos.")
    return isbn


@dataclass
class Book:
    id: str
    title: str
    author: str
    isbn: str
    borrower: Optional[str] = None

    @classmethod
    def create(cls, title: str, author: str, isbn: str) -> "Book":
        return cls(
            id=str(uuid4()),
            title=_require_text(title, "título"),
            author=_require_text(author, "autor"),
            isbn=_normalize_isbn(isbn),
        )

    @property
    def is_available(self) -> bool:
        return self.borrower is None

    def lend_to(self, borrower: str) -> None:
        if not self.is_available:
            raise BookAlreadyLentError(self.borrower)
        self.borrower = _require_text(borrower, "prestatario")

    def give_back(self) -> None:
        if self.is_available:
            raise BookNotLentError()
        self.borrower = None

"""Casos de uso (puertos de entrada). Orquestan el dominio; no conocen Flask ni SQL."""
from dataclasses import dataclass
from typing import List

from ..domain.book import Book
from ..domain.errors import BookNotFoundError, DuplicateIsbnError
from .ports import BookRepository


def _get_book_or_fail(books: BookRepository, book_id: str) -> Book:
    book = books.find_by_id(book_id)
    if book is None:
        raise BookNotFoundError(book_id)
    return book


@dataclass
class RegisterBook:
    books: BookRepository

    def execute(self, title: str, author: str, isbn: str) -> Book:
        book = Book.create(title, author, isbn)
        if self.books.find_by_isbn(book.isbn):
            raise DuplicateIsbnError(book.isbn)
        self.books.save(book)
        return book


@dataclass
class ListBooks:
    books: BookRepository

    def execute(self) -> List[Book]:
        return sorted(self.books.find_all(), key=lambda b: b.title.lower())


@dataclass
class LendBook:
    books: BookRepository

    def execute(self, book_id: str, borrower: str) -> Book:
        book = _get_book_or_fail(self.books, book_id)
        book.lend_to(borrower)
        self.books.save(book)
        return book


@dataclass
class ReturnBook:
    books: BookRepository

    def execute(self, book_id: str) -> Book:
        book = _get_book_or_fail(self.books, book_id)
        book.give_back()
        self.books.save(book)
        return book


@dataclass
class UseCases:
    """Agrupa los casos de uso para inyectarlos en el adaptador web."""
    register: RegisterBook
    list_all: ListBooks
    lend: LendBook
    give_back: ReturnBook

    @classmethod
    def build(cls, books: BookRepository) -> "UseCases":
        return cls(RegisterBook(books), ListBooks(books), LendBook(books), ReturnBook(books))

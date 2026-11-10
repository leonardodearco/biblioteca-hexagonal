import pytest

from library.domain.book import Book
from library.domain.errors import BookAlreadyLentError, BookNotLentError, InvalidBookError


def make_book() -> Book:
    return Book.create("Cien años de soledad", "Gabriel García Márquez", "978-0-06-088328-7")


def test_create_normalizes_isbn():
    assert make_book().isbn == "9780060883287"


@pytest.mark.parametrize("title,author,isbn", [("", "A", "1234567890"), ("T", " ", "1234567890"), ("T", "A", "123")])
def test_create_rejects_invalid_data(title, author, isbn):
    with pytest.raises(InvalidBookError):
        Book.create(title, author, isbn)


def test_lend_and_return_cycle():
    book = make_book()
    book.lend_to("Ana")
    assert not book.is_available
    book.give_back()
    assert book.is_available


def test_cannot_lend_twice():
    book = make_book()
    book.lend_to("Ana")
    with pytest.raises(BookAlreadyLentError):
        book.lend_to("Luis")


def test_cannot_return_available_book():
    with pytest.raises(BookNotLentError):
        make_book().give_back()

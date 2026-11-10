"""Adaptador de entrada: traduce HTTP <-> casos de uso."""
from flask import Flask, jsonify, request

from ...application.use_cases import UseCases
from ...domain.book import Book
from ...domain.errors import (
    BookAlreadyLentError,
    BookNotFoundError,
    BookNotLentError,
    DomainError,
    DuplicateIsbnError,
    InvalidBookError,
)

HTTP_STATUS_BY_ERROR = {
    InvalidBookError: 400,
    BookNotFoundError: 404,
    DuplicateIsbnError: 409,
    BookAlreadyLentError: 409,
    BookNotLentError: 409,
}


def book_to_dict(book: Book) -> dict:
    return {
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "isbn": book.isbn,
        "borrower": book.borrower,
        "available": book.is_available,
    }


def create_app(use_cases: UseCases) -> Flask:
    app = Flask(__name__)
    _register_routes(app, use_cases)
    _register_error_handlers(app)
    return app


def _register_routes(app: Flask, use_cases: UseCases) -> None:
    @app.get("/api/books")
    def list_books():
        return jsonify([book_to_dict(b) for b in use_cases.list_all.execute()])

    @app.post("/api/books")
    def register_book():
        data = request.get_json(silent=True) or {}
        book = use_cases.register.execute(
            data.get("title"), data.get("author"), data.get("isbn")
        )
        return jsonify(book_to_dict(book)), 201

    @app.post("/api/books/<book_id>/lend")
    def lend_book(book_id: str):
        data = request.get_json(silent=True) or {}
        book = use_cases.lend.execute(book_id, data.get("borrower"))
        return jsonify(book_to_dict(book))

    @app.post("/api/books/<book_id>/return")
    def return_book(book_id: str):
        return jsonify(book_to_dict(use_cases.give_back.execute(book_id)))


def _register_error_handlers(app: Flask) -> None:
    @app.errorhandler(DomainError)
    def handle_domain_error(error: DomainError):
        status = HTTP_STATUS_BY_ERROR.get(type(error), 400)
        return jsonify({"error": str(error)}), status

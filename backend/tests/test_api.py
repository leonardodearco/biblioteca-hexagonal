import pytest

from library.application.use_cases import UseCases
from library.infrastructure.persistence.in_memory_book_repository import InMemoryBookRepository
from library.infrastructure.persistence.sqlite_book_repository import SqliteBookRepository
from library.infrastructure.web.flask_api import create_app


@pytest.fixture(params=["memory", "sqlite"])
def client(request):
    repo = InMemoryBookRepository() if request.param == "memory" else SqliteBookRepository(":memory:")
    return create_app(UseCases.build(repo)).test_client()


def create_book(client, isbn="1234567890"):
    return client.post("/api/books", json={"title": "Aura", "author": "Fuentes", "isbn": isbn})


def test_full_flow(client):
    book = create_book(client).get_json()
    assert client.post(f"/api/books/{book['id']}/lend", json={"borrower": "Ana"}).get_json()["available"] is False
    assert client.post(f"/api/books/{book['id']}/return").get_json()["available"] is True
    assert len(client.get("/api/books").get_json()) == 1


def test_errors_are_mapped_to_http_status(client):
    assert client.post("/api/books", json={"title": ""}).status_code == 400
    assert create_book(client).status_code == 201
    assert create_book(client).status_code == 409
    assert client.post("/api/books/x/return").status_code == 404

import pytest

from library.application.use_cases import UseCases
from library.domain.errors import BookNotFoundError, DuplicateIsbnError
from library.infrastructure.persistence.in_memory_book_repository import InMemoryBookRepository


@pytest.fixture
def use_cases():
    return UseCases.build(InMemoryBookRepository())


def test_register_and_list_sorted_by_title(use_cases):
    use_cases.register.execute("Zorba", "Kazantzakis", "1234567890")
    use_cases.register.execute("Aura", "Fuentes", "0987654321")
    assert [b.title for b in use_cases.list_all.execute()] == ["Aura", "Zorba"]


def test_register_rejects_duplicate_isbn(use_cases):
    use_cases.register.execute("A", "B", "1234567890")
    with pytest.raises(DuplicateIsbnError):
        use_cases.register.execute("C", "D", "123-456-7890")


def test_lend_persists_state(use_cases):
    book = use_cases.register.execute("A", "B", "1234567890")
    use_cases.lend.execute(book.id, "Ana")
    assert use_cases.list_all.execute()[0].borrower == "Ana"


def test_unknown_book_raises(use_cases):
    with pytest.raises(BookNotFoundError):
        use_cases.give_back.execute("no-existe")

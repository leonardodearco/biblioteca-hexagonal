"""Puertos de salida: contratos que la infraestructura debe cumplir."""
from abc import ABC, abstractmethod
from typing import List, Optional

from ..domain.book import Book


class BookRepository(ABC):
    @abstractmethod
    def save(self, book: Book) -> None: ...

    @abstractmethod
    def find_by_id(self, book_id: str) -> Optional[Book]: ...

    @abstractmethod
    def find_by_isbn(self, isbn: str) -> Optional[Book]: ...

    @abstractmethod
    def find_all(self) -> List[Book]: ...

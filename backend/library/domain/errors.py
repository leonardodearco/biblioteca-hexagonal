"""Errores del dominio. No dependen de ningún framework."""


class DomainError(Exception):
    """Clase base de todas las reglas de negocio violadas."""


class InvalidBookError(DomainError):
    pass


class DuplicateIsbnError(DomainError):
    def __init__(self, isbn: str):
        super().__init__(f"Ya existe un libro con el ISBN {isbn}.")


class BookNotFoundError(DomainError):
    def __init__(self, book_id: str):
        super().__init__(f"No existe un libro con id {book_id}.")


class BookAlreadyLentError(DomainError):
    def __init__(self, borrower: str):
        super().__init__(f"El libro ya está prestado a {borrower}.")


class BookNotLentError(DomainError):
    def __init__(self):
        super().__init__("El libro no está prestado, no se puede devolver.")

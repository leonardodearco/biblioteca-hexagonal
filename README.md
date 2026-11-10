# Biblioteca de barrio — Aplicación web con Arquitectura Hexagonal

Aplicación web (backend + frontend) para **registrar libros y controlar sus préstamos**.
Proyecto de la actividad *"Diseñar Aplicación Moderna Orientada a la Web"*.

| Capa | Tecnología |
|------|------------|
| Backend | Python 3 + **Flask** |
| Frontend | **React** + Vite |
| Base de datos | **SQLite** (relacional) |
| Pruebas | pytest (15 pruebas) |

## 1. Problema que resuelve
Una biblioteca pequeña necesita saber qué libros tiene y quién tiene prestado cada uno.
Reglas de negocio:
- Un libro requiere título, autor e ISBN válido (10 o 13 dígitos).
- No pueden existir dos libros con el mismo ISBN.
- Un libro prestado no se puede volver a prestar.
- Solo se puede devolver un libro que esté prestado.

## 2. Arquitectura Hexagonal (Puertos y Adaptadores)

```
        ADAPTADORES DE ENTRADA                    ADAPTADORES DE SALIDA
     (quien usa la aplicación)                (lo que la aplicación usa)

   ┌────────────────┐        ┌──────────────────────────────┐        ┌───────────────────────────┐
   │  API REST Flask│ ─────▶ │  APLICACIÓN (casos de uso)   │ ─────▶ │ SqliteBookRepository      │
   │  flask_api.py  │        │  RegisterBook, LendBook ...  │  puerto│ InMemoryBookRepository    │
   └────────────────┘        │            │                 │  salida└───────────────────────────┘
                             │            ▼                 │  BookRepository
                             │  DOMINIO: Book + reglas      │
                             └──────────────────────────────┘
```

```
backend/library/
├── domain/                 # Núcleo: entidad Book y errores. Sin dependencias externas.
├── application/
│   ├── ports.py            # Puerto de salida: BookRepository (interfaz)
│   └── use_cases.py        # Casos de uso: RegisterBook, ListBooks, LendBook, ReturnBook
└── infrastructure/
    ├── persistence/        # Adaptadores de salida: SQLite y en memoria
    └── web/flask_api.py    # Adaptador de entrada: HTTP -> casos de uso
backend/app.py              # Raíz de composición: conecta puertos con adaptadores
```

**Regla de dependencia:** las flechas solo apuntan hacia el dominio. `domain` no importa nada de
`application`, y `application` no importa nada de `infrastructure`. Prueba de que funciona: los
mismos tests de la API corren contra SQLite **y** contra memoria sin cambiar una línea del negocio.

El frontend sigue la misma idea: `components` (UI) → `hooks/useBooks` (lógica) → `api/httpBookApi` (adaptador HTTP).
El adaptador se inyecta desde `main.jsx`, por lo que se puede reemplazar por un mock en pruebas.

## 3. Principios SOLID (dónde se evidencian)

| Principio | Evidencia |
|-----------|-----------|
| **S** – Responsabilidad única | Cada caso de uso hace una sola cosa; `flask_api.py` solo traduce HTTP; `Book` solo contiene reglas del libro. En React, `BookForm` captura datos y `useBooks` gestiona el estado. |
| **O** – Abierto/Cerrado | Para añadir PostgreSQL basta crear otra clase que implemente `BookRepository`; ningún caso de uso se modifica. `HTTP_STATUS_BY_ERROR` permite añadir errores sin tocar los handlers. |
| **L** – Sustitución de Liskov | `InMemoryBookRepository` y `SqliteBookRepository` son intercambiables en cualquier lugar donde se espera un `BookRepository` (ver `tests/test_api.py`, parametrizado con ambos). |
| **I** – Segregación de interfaces | `BookRepository` expone solo 4 operaciones y cada caso de uso es una clase con un único método `execute`. |
| **D** – Inversión de dependencias | Los casos de uso reciben el `BookRepository` abstracto por constructor; la implementación concreta se elige solo en `app.py`. |

## 4. Código limpio
- Nombres que expresan intención (`lend_to`, `give_back`, `is_available`).
- Funciones pequeñas con un solo nivel de abstracción.
- Sin números ni textos mágicos: `ISBN_LENGTHS`, `HTTP_STATUS_BY_ERROR`.
- Errores de dominio propios en lugar de `ValueError` genéricos.
- Pruebas que documentan el comportamiento esperado.

## 5. Refactoring aplicado (evidencia)

**a) Extraer función — validaciones repetidas.**
Antes, `Book.create` repetía el `if not value.strip(): raise ...` para cada campo. Ahora existe `_require_text` y `_normalize_isbn`.

**b) Eliminar duplicación — buscar libro o fallar.**
Antes, `LendBook` y `ReturnBook` repetían `find_by_id` + `if None: raise BookNotFoundError`. Se extrajo `_get_book_or_fail`.

**c) Reemplazar condicionales por tabla.**
Antes, el adaptador web usaba una cadena de `if isinstance(error, ...)`. Ahora usa el diccionario `HTTP_STATUS_BY_ERROR`.

**d) Mover lógica a donde pertenece.**
Antes, el caso de uso comprobaba `if book.borrower is not None`. Ahora la entidad decide (`is_available`, `lend_to`), para que la regla viva en un solo lugar.

## 6. Cómo ejecutarlo

**Backend**
```bash
cd backend
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m pytest        # 15 pruebas
python app.py           # http://localhost:5000
```

**Frontend** (en otra terminal)
```bash
cd frontend
npm install
npm run dev             # http://localhost:5173  (proxy a :5000)
```

## 7. API REST

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/books` | Lista los libros ordenados por título |
| POST | `/api/books` | Registra un libro `{title, author, isbn}` |
| POST | `/api/books/<id>/lend` | Presta el libro `{borrower}` |
| POST | `/api/books/<id>/return` | Registra la devolución |

Códigos de error: `400` datos inválidos · `404` libro no existe · `409` conflicto de regla de negocio.

## 8. Subir a GitHub / GitLab
```bash
git init
git add .
git commit -m "Biblioteca con arquitectura hexagonal"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/biblioteca-hexagonal.git
git push -u origin main
```

import BookItem from "./BookItem.jsx";

export default function BookList({ books, onLend, onReturn }) {
  if (books.length === 0) {
    return <p className="empty">Aún no hay libros. Añade el primero con el formulario.</p>;
  }
  return (
    <ul className="book-list">
      {books.map((book) => (
        <BookItem key={book.id} book={book} onLend={onLend} onReturn={onReturn} />
      ))}
    </ul>
  );
}

import { useState } from "react";

export default function BookItem({ book, onLend, onReturn }) {
  const [borrower, setBorrower] = useState("");

  const lend = async (e) => {
    e.preventDefault();
    if (await onLend(book.id, borrower)) setBorrower("");
  };

  return (
    <li className={book.available ? "book" : "book lent"}>
      <div>
        <h2>{book.title}</h2>
        <p>{book.author} · ISBN {book.isbn}</p>
      </div>

      {book.available ? (
        <form onSubmit={lend} className="lend-form">
          <input value={borrower} onChange={(e) => setBorrower(e.target.value)} placeholder="Nombre de quien lo lleva" aria-label="Prestatario" required />
          <button type="submit">Prestar</button>
        </form>
      ) : (
        <div className="lend-form">
          <span>Lo tiene {book.borrower}</span>
          <button onClick={() => onReturn(book.id)}>Registrar devolución</button>
        </div>
      )}
    </li>
  );
}

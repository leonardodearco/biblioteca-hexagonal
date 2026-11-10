import { useBooks } from "./hooks/useBooks.js";
import BookForm from "./components/BookForm.jsx";
import BookList from "./components/BookList.jsx";

export default function App({ api }) {
  const { books, error, register, lend, giveBack } = useBooks(api);

  return (
    <main className="page">
      <header>
        <h1>Biblioteca de barrio</h1>
        <p>Registra libros y controla quién los tiene.</p>
      </header>

      {error && <p role="alert" className="error">{error}</p>}

      <BookForm onSubmit={register} />
      <BookList books={books} onLend={lend} onReturn={giveBack} />
    </main>
  );
}

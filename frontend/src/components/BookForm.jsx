import { useState } from "react";

const EMPTY = { title: "", author: "", isbn: "" };

export default function BookForm({ onSubmit }) {
  const [form, setForm] = useState(EMPTY);

  const update = (field) => (e) => setForm({ ...form, [field]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (await onSubmit(form)) setForm(EMPTY);
  };

  return (
    <form onSubmit={handleSubmit} className="book-form">
      <label>Título<input value={form.title} onChange={update("title")} required /></label>
      <label>Autor<input value={form.author} onChange={update("author")} required /></label>
      <label>ISBN<input value={form.isbn} onChange={update("isbn")} placeholder="10 o 13 dígitos" required /></label>
      <button type="submit">Añadir libro</button>
    </form>
  );
}

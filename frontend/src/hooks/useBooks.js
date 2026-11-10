import { useCallback, useEffect, useState } from "react";

export function useBooks(api) {
  const [books, setBooks] = useState([]);
  const [error, setError] = useState("");

  const refresh = useCallback(async () => {
    try {
      setBooks(await api.list());
    } catch (e) {
      setError(e.message);
    }
  }, [api]);

  useEffect(() => {
    refresh();
  }, [refresh]);

  const runAndRefresh = async (action) => {
    setError("");
    try {
      await action();
      await refresh();
      return true;
    } catch (e) {
      setError(e.message);
      return false;
    }
  };

  return {
    books,
    error,
    register: (book) => runAndRefresh(() => api.register(book)),
    lend: (id, borrower) => runAndRefresh(() => api.lend(id, borrower)),
    giveBack: (id) => runAndRefresh(() => api.giveBack(id)),
  };
}

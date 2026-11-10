async function request(path, options = {}) {
  const response = await fetch(`/api/books${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || "Error inesperado");
  return data;
}

const post = (path, body) =>
  request(path, { method: "POST", body: JSON.stringify(body ?? {}) });

export const httpBookApi = {
  list: () => request(""),
  register: (book) => post("", book),
  lend: (id, borrower) => post(`/${id}/lend`, { borrower }),
  giveBack: (id) => post(`/${id}/return`),
};

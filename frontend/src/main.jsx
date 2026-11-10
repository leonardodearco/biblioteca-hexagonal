import React from "react";
import { createRoot } from "react-dom/client";
import App from "./App.jsx";
import { httpBookApi } from "./api/httpBookApi.js";
import "./styles.css";

// Raíz de composición del frontend: aquí se elige el adaptador concreto.
createRoot(document.getElementById("root")).render(<App api={httpBookApi} />);

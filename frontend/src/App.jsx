import React, { useState } from "react";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import VerseSearch from "./components/VerseSearch";
import "./App.css"

const App = () => {
  return (
    <div>
      <h1>Ask a Question!</h1>
      <VerseSearch />
      <ToastContainer position="top-center" autoClose={3000} />
    </div>
  );
};

export default App;

import React, { useState } from "react";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import VerseSearch from "./components/VerseSearch";

const App = () => {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100 p-4">
      <h1 className="text-2xl font-bold mb-4">Ask a Question</h1>
      <VerseSearch/>
      <ToastContainer position="top-center" autoClose={3000} />
    </div>
  );
};

export default App;

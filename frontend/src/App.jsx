import React, { useState } from "react";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
// import VerseSearch from "./components/VerseSearch";
import "./css/App.css"
import { Routes,Route } from "react-router-dom"
import NavBar from "./components/NavBar";
import VerseSearch from "./components/VerseSearch";
import Summarize from "./components/Summarize";
import "./css/index.css"


const App = () => {
  return (
    <div>
      <NavBar />
      <Routes>
        <Route path = "/" element={<VerseSearch />} />
        <Route path = "/summary" element={<Summarize />} />
      </Routes>
    </div>
  );
};

export default App;


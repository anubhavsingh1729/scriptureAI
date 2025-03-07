import React, { useState } from "react";
import api from "../api";

const VerseSearch = () => {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!query.trim()) {
      alert("Please enter a query!");
      return;
    }
    setLoading(true);
    setResults([]);
    try {
      const response = await api.get("/verses", { params: { query } });
      setResults(response.data.results);
    } catch (error) {
      alert("Error fetching verses. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>Bible Search Verses</h1>
      
      <div className="search-container">
      <input
        type="text"
        className="search-box"
        placeholder="Enter text..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <div className="button-container">
        <button className="search-button" onClick={handleSubmit} disabled={loading}>
            {loading ? "Searching..." : "Search"}
        </button>
      </div>
      </div>
      {results.length > 0 && (
        <div className="results-container">
          <strong>Verses:</strong>
          <ul>
            {results.map((verse, index) => (
              <li key={index}>{verse}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default VerseSearch;
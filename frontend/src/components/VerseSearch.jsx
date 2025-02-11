import React, { useState } from "react";
import api from "../api";
import axios from "axios";

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
    <div className="w-full max-w-md bg-white p-6 rounded-lg shadow-lg">
      <input
        type="text"
        className="w-full p-2 border rounded mb-4"
        placeholder="Enter your query..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <button
        className="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600"
        onClick={handleSubmit}
        disabled={loading}
      >
        {loading ? "Searching..." : "Search"}
      </button>
      {results.length > 0 && (
        <div className="mt-4 p-3 bg-green-100 border-l-4 border-green-500 rounded">
          <strong>Results:</strong>
          <ul className="list-disc ml-4">
            {results.map((verse, index) => (
              <li key={index} className="mt-2">{verse}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default VerseSearch;
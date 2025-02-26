import React, { useState } from "react";
import { use } from "react";
import api from "../api";

const Commentary = () => {

    const [commentaries, setCommentaries] = useState([]);
    const [query, setQuery] = useState("");
    const [loading, setLoading] = useState(false);

    const handleSubmit = async () => {
        if(!query.trim()) {
            alert("Please enter a query!");
            return;
        }
        setLoading(true);
        setCommentaries([]);
        try {
            const response = await api.get("/commentary", {params : { query } });
            setCommentaries(response.data.results);
        } catch (error) {
            alert ("Error");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
          <h1>Bible Search Commentaries</h1>
          <input
            type="text"
            className="search-box"
            placeholder="Get answer from Commentaries..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          
          <button className="search-button" onClick={handleSubmit} disabled={loading}>
            {loading ? "Searching..." : "Search"}
          </button>
    
          {commentaries.length > 0 && (
            <div className="results-container">
              <strong>Commentaries related to "{query}":</strong>
              <ul>
                {commentaries.map((comm, index) => (
                  <li key={index}>{comm}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      );
};

export default Commentary
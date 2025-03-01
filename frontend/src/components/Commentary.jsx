import React, { useState } from "react";
import { use } from "react";
import api from "../api";

const Commentary = () => {

    const [commentaries, setCommentaries] = useState([]);
    const [summary, setSummary] = useState("");
    const [query, setQuery] = useState("");
    const [loading, setLoading] = useState(false);
    const [showPopup, setShowPopup] = useState(false);

    const handleSubmit = async () => {
        if(!query.trim()) {
            alert("Please enter a query!");
            return;
        }
        setLoading(true);
        setCommentaries([]);
        setShowPopup(false);
        try {
            const response = await api.get("/commentary", {params : { query } });
            setCommentaries(response.data.commentaries);
            setSummary(response.data.answer);
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
          {summary && (<div className="results-container">
            <strong>Summary of Commentaries:</strong>
            <p>{summary}</p>
          </div>)}

          {commentaries.length > 0 && (
                <button className="show-button" onClick={() => setShowPopup(true)}>
                    Show Commentaries
                </button>
            )}

            {/* Popup Modal for Commentaries */}
            {showPopup && (
                <div className="modal-overlay">
                    <div className="modal">
                        <h2>Commentaries</h2>
                        <div className="modal-content">
                            <ul>
                                {commentaries.map((comm, index) => (
                                    <li key={index}>{comm}</li>
                                ))}
                            </ul>
                        </div>
                        <button className="close-button" onClick={() => setShowPopup(false)}>Close</button>
                    </div>
                </div>
            )}

          {/* {commentaries.length > 0 && (
            <div className="results-container">
              <strong>Commentaries:</strong>
              <ul>
                {commentaries.map((comm, index) => (
                  <li key={index}>{comm}</li>
                ))}
              </ul>
            </div>
          )} */}

        </div>
      );
};

export default Commentary
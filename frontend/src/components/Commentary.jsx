import React, { useState } from "react";
import api from "../api";

const Commentary = () => {
    const [commentaries, setCommentaries] = useState([]);
    const [summary, setSummary] = useState("");
    const [query, setQuery] = useState("");
    const [loadingSummary, setLoadingSummary] = useState(false);
    const [loadingCommentaries, setLoadingCommentaries] = useState(false)
    const [showPopup, setShowPopup] = useState(false);

    const getSummary = async () => {
        if (!query.trim()) {
            alert("Please enter a query!");
            return;
        }
        setLoadingSummary(true);
        try {
            const response = await api.get("/summary", { params: { query } });
            setSummary(response.data.answer);
            setShowPopup(true);
        } catch (error) {
            alert("Error fetching summary");
        } finally {
            setLoadingSummary(false);
        }
    };

    const getCommentary = async () => {
        if (!query.trim()) {
            alert("Please enter a query!");
            return;
        }
        setLoadingCommentaries(true);
        setSummary(""); 
        setShowPopup(false);
        try {
            const response = await api.get("/commentary", { params: { query } });
            setCommentaries(response.data.results);
        } catch (error) {
            alert("Error fetching commentary");
        } finally {
            setLoadingCommentaries(false);
        }
    };

    return (
        <div className="container">
        <h1>Bible Search Commentaries</h1>
        
            <div className="search-container">
                <input
                    type="text"
                    className="search-box"
                    placeholder="Enter text..."
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                />

                <div className="button-container">
                    <button className="search-button" onClick={getSummary} disabled={loadingSummary}>
                        {loadingSummary ? "Summarizing..." : "Summary"}
                    </button>
                    
                    <button className="search-button" onClick={getCommentary} disabled={loadingCommentaries}>
                        {loadingCommentaries ? "Searching..." : "Commentary"}
                    </button>
                </div>
            </div>

            {commentaries.length > 0 && (
                <div className="results-container">
                    <h2 style={{ color: "white" }}>Commentaries</h2>
                    <ul>
                        {commentaries.map((comm, index) => (
                            <li key={index} style={{ color: "white" }}>
                                <strong>{comm.verse}: {comm.text}</strong>
                                <ul>
                                    {comm.commentaries.map((com, subindex) => (
                                        <li key={subindex} style={{ color: "white" }}>{com}</li>
                                    ))}
                                </ul>
                            </li>
                        ))}
                    </ul>
                </div>
            )}

            {showPopup && (
                            <div className="modal-overlay">
                                <div className="modal">
                                    <h2>Summary</h2>
                                    <p>{summary}</p>
                                    <button className="close-button" onClick={() => setShowPopup(false)}>Close</button>
                                </div>
                            </div>
                        )}
        </div>
    );
};

export default Commentary;
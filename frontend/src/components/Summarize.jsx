import React, { useState } from "react";

const Summarize = () => {

    const [summary, setSummary] = useState("");

    const getSummary = () => {
        setSummary("summary of the chapter")
    }

    return(
        <div>
            <h1>Chapter Summary</h1>
            <button className="search-button" onClick={getSummary}>Summarize</button>
            <p>{summary}</p>
        </div>
    );

};

export default Summarize
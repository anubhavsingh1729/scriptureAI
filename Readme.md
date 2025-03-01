# ScriptureLM

A lightweight application for semantic Bible verse search and commentary summarization. The project uses **FastAPI**, **FAISS**, and **Sentence Transformers** on the backend for semantic search, and **React** with **React Router** on the frontend for an intuitive user interface. It also leverages a **Long T5** model to summarize commentary text.

---

## Project Overview

- **Search Verses:** Enter a query/keywords to retrieve relevant Bible verses.  
- **Commentary Summaries:** Fetch commentary passages related to your query, then generate a concise summary via an LLM (Long T5).  
- **Data & Indexes:** Precomputed FAISS indexes (`faiss_index.bin` for verses, `comm_index.bin` for commentaries) are stored in the `data/` folder.  

The backend (`backend/`) handles all AI-related tasks (semantic search, summarization), while the frontend (`frontend/`) provides a simple, user-friendly interface.

---

## File Structure (High-Level)

```
.
├── data/
│   ├── corpus.json          # Verse corpus
│   ├── comm_corpus.json     # Commentary corpus
│   ├── faiss_index.bin      # FAISS index for verses
│   └── comm_index.bin       # FAISS index for commentaries
├── backend/
│   ├── app.py               # FastAPI application
│   └── test.py              # (Optional) test script
└── frontend/
    ├── src/
    │   ├── components/
    │   │   ├── NavBar.jsx
    │   │   ├── VerseSearch.jsx
    │   │   └── Commentary.jsx
    │   ├── App.jsx
    │   └── index.css
    ├── public/
    ├── package.json
    └── ...
```

---

## How to Run

### 1. Backend (FastAPI)

1. **Install Python dependencies** (e.g., FastAPI, Uvicorn, FAISS, Sentence Transformers, Transformers).  
2. In the `backend/` directory, run:
   ```bash
   uvicorn app:app --reload
   ```
3. The API will be accessible at localhost

### 2. Frontend (React)

1. **Install Node dependencies** in `frontend/`:
   ```bash
   npm install
   ```
2. **Start the development server**:
   ```bash
   npm start
   ```

---

## Usage

- **Verse Search**  
  - Navigate to the Home page (`"/"`)  
  - Enter a query and click **Search**  
  - View matching verses

- **Commentary Summaries**  
  - Go to the **Commentary** page (`"/commentary"`)  
  - Enter a query and click **Search**  
  - Read the generated summary and, optionally, display the full commentary passages

---

## Notes & Customization

- **Data & Indexes:** The project expects precomputed FAISS indexes in `data/`. If you modify or replace the corpora (`corpus.json`, `comm_corpus.json`), you must rebuild the indexes accordingly.  
- **LLM Model:** By default, the project uses `google/long-t5-tglobal-base` for summarization. Adjust in `app.py` as needed.  
- **CORS:** Currently open to all origins (`allow_origins=["*"]`). For production, restrict this to your domain.

---

## License

Feel free to adapt or extend this project as needed. Check the repository for any specific license information.

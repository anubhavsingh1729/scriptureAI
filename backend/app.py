from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import json

app = FastAPI()

# Enable CORS so the React app can call the API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow access from frontend. For production, restrict this to your frontend’s domain.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"a":"b"}

model = SentenceTransformer("all-MiniLM-L6-v2")

index = faiss.read_index("../data/faiss_index.bin")

comm_index = faiss.read_index("../data/comm_index.bin")

with open("../data/corpus.json", "r") as f:
    corpus = json.load(f)

with open("../data/comm_corpus.json", "r") as f:
    comm_corpus = json.load(f)

class SearchRequest(BaseModel):
    query: str


# @app.post("/api/search")
# async def search(req: SearchRequest):
#     query = req.query.strip()
#     if not query:
#         raise HTTPException(status_code=400, detail="Query is required.")
    
#     # Compute embedding for the user query
#     query_embedding = model.encode([query], convert_to_numpy=True)
#     query_embedding = query_embedding / np.linalg.norm(query_embedding, axis=1, keepdims=True)
    
#     # Retrieve the top 5 matching verses
#     k = 5
#     distances, indices = index.search(query_embedding, k)
#     results = []
#     for score, idx in zip(distances[0], indices[0]):
#         verse = corpus[idx]
#         verse['score'] = float(score)
#         results.append(verse)
    
#     return {"results": results}

@app.get("/verses")
def query(query: str):
    # Compute embedding for the user query
    query_embedding = model.encode([query], convert_to_numpy=True)
    query_embedding = query_embedding / np.linalg.norm(query_embedding, axis=1, keepdims=True)
    
    # Retrieve the top 5 matching verses
    k = 5
    distances, indices = index.search(query_embedding, k)
    results = []
    for score, idx in zip(distances[0], indices[0]):
        verse = corpus[idx]
        #verse['score'] = float(score)
        results.append(verse)
    
    return {"results": results}

@app.get("/commentary")
def commentary(query: str):
    query_emb = model.encode([query],convert_to_numpy=True)
    query_emb = query_emb / np.linalg.norm(query_emb, axis=1, keepdims=True)

    k=5
    distances, indices = comm_index.search(query_emb, k)
    results = []
    for score, idx in zip(distances[0], indices[0]):
        comm = comm_corpus[idx]
        #verse['score'] = float(score)
        results.append(comm.replace('/n',''))

    return {"results": results}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

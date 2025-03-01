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

#Sentence Transformer===========================================================================================
model = SentenceTransformer("all-MiniLM-L6-v2")

index = faiss.read_index("../data/faiss_index.bin")

comm_index = faiss.read_index("../data/comm_index.bin")

with open("../data/corpus.json", "r") as f:
    corpus = json.load(f)

with open("../data/comm_corpus.json", "r") as f:
    comm_corpus = json.load(f)

class SearchRequest(BaseModel):
    query: str
#================================================================================================================

# define LLM model

# from transformers import BartForConditionalGeneration, BartTokenizer
# model_name = 'facebook/bart-large-cnn'
# tokenizer=BartTokenizer.from_pretrained(model_name)
# llm_model = BartForConditionalGeneration.from_pretrained(model_name)

from transformers import AutoTokenizer, LongT5ForConditionalGeneration
t5tokenizer = AutoTokenizer.from_pretrained("google/long-t5-tglobal-base")
t5model = LongT5ForConditionalGeneration.from_pretrained("google/long-t5-tglobal-base")

#helper functions for commentary summarisation: -----------------------------------
def summarize(text,tokenizer,model,sumlen=500,token_len=1024):
    tokens = tokenizer.encode(
        "summarize: "+text,
        return_tensors='pt',
        max_length=token_len,
        truncation = True
    )

    outputs = model.generate(
        tokens,
        max_length=sumlen,
        min_length=sumlen//2,
        length_penalty=1,
        early_stopping=True,
        no_repeat_ngram_size=3,
        
        num_beams=5,
        top_k=50,
        top_p=0.92,
        temperature=0.7
    )
    
    summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return summary

def split_text(text,tokenizer,max_tokens=900,overlap_per = 10):
    tokens = tokenizer.tokenize(text)
    
    overlap_len = int(max_tokens*overlap_per /100)
    
    chunks = [tokens[i:i+max_tokens] for i in range(0,len(tokens),max_tokens-overlap_len)]
    
    texts = [tokenizer.decode(
        tokenizer.convert_tokens_to_ids(chunk),skip_special_token=True
    ) for chunk in chunks]
    
    return texts

def recursive_summarize(text, tokenizer, model, target_length=500, chunk_size=900):
    while len(text.split()) > target_length:
        chunks = split_text(text, tokenizer, max_tokens=chunk_size)
        summaries = [summarize(chunk, tokenizer, model, sumlen=target_length // 2) for chunk in chunks]
        text = " ".join(summaries)  
    
    return summarize(text, tokenizer, model, sumlen=target_length)
#-----------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------

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

#@app.get("/commentary")
def commentary(query: str,k=5):
    query_emb = model.encode([query],convert_to_numpy=True)
    query_emb = query_emb / np.linalg.norm(query_emb, axis=1, keepdims=True)

    distances, indices = comm_index.search(query_emb, k)
    results = []
    for score, idx in zip(distances[0], indices[0]):
        comm = comm_corpus[idx]
        #verse['score'] = float(score)
        results.append(comm.replace('/n',''))

    return {"results": results}

#use commentaries and summarize them to form an answer for the user query
@app.get("/commentary")
def get_answer(query: str):
    results = commentary(query,k=5)['results']
    commentaries = ''.join(results)
    #summary = recursive_summarize(commentaries,tokenizer,llm_model)
    summary = summarize(commentaries, t5tokenizer, t5model, sumlen=500,token_len=5000)
    return {"answer":summary,"commentaries":results}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

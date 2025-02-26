from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import json

model = SentenceTransformer("all-MiniLM-L6-v2")


comm_index = faiss.read_index("../data/comm_index.bin")

print(comm_index.ntotal)

print("Index dimension:", comm_index.d)

with open("../data/comm_corpus.json", "r") as f:
    comm_corpus = json.load(f)

query = input()

query_emb = model.encode([query],convert_to_numpy=True)
query_emb = query_emb / np.linalg.norm(query_emb, axis=1, keepdims=True)


print("Query embedding dimension:", query_emb.shape[1])

k=5
distances, indices = comm_index.search(query_emb, k)
results = []
for score, idx in zip(distances[0], indices[0]):
    comm = comm_corpus[idx]
    #verse['score'] = float(score)
    results.append(comm)

print(distances)
print(indices)
print("random",comm_index.reconstruct(0)) 
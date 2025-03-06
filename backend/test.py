from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import json

query = input()

model = SentenceTransformer("all-MiniLM-L6-v2")

bibleindex = faiss.read_index("../data/bibleindex.bin")

print(bibleindex.ntotal)


with open("../data/biblecorpus.json", "r") as f:
    biblecorpus = json.load(f)

query_emb = model.encode([query],convert_to_numpy=True)
query_emb = query_emb / np.linalg.norm(query_emb, axis=1, keepdims=True)


k=2
distances, indices = bibleindex.search(query_emb, k)

results = [biblecorpus[i] for i in indices[0]]

#print([res['text'] for res in results])
print(results)

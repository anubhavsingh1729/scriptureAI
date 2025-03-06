import torch
from sentence_transformers import SentenceTransformer
import pandas as pd
import faiss
import json
from collections import defaultdict

df = pd.read_csv("../data/text_with_commentary.csv")

device = 'cuda' if torch.cuda.is_available() else 'cpu'

# Initialize a pre-trained SentenceTransformer for embeddings
model = SentenceTransformer('all-MiniLM-L6-v2', device=device)

# Dictionary to aggregate commentaries per unique text
metadata_dict = defaultdict(lambda: {"verse": "", "commentaries": []})

# create metadata from bible text
for _, row in df.iterrows():
    text = row["text"]
    verse = row["verse"]
    commentary_entry = f"{row['father_name']}: {row['commentary']}"

    # Initialize verse if not set
    if not metadata_dict[text]["verse"]:
        metadata_dict[text]["verse"] = verse

    # Append the commentary
    metadata_dict[text]["commentaries"].append(commentary_entry)

# Convert dictionary to a list of dictionaries
metadata = [{"text": text, "verse": data["verse"], "commentaries": data["commentaries"]}
            for text, data in metadata_dict.items()]

# save corpus as json
with open("../data/biblecorpus.json", "w") as f:
    json.dump(metadata, f)

# create embeddings
data = []
for i in metadata:
    data.append(i['verse']+': '+i['text'])

embeddings = model.encode(data, convert_to_numpy=True)

# Build FAISS index
d = embeddings.shape[1] 
index = faiss.IndexFlatL2(d)
index.add(embeddings)

# Save FAISS index
faiss.write_index(index, "../data/bibleindex.bin")
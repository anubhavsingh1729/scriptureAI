import re
from collections import defaultdict
import pandas as pd
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import json

embedder = SentenceTransformer("all-MiniLM-L6-v2")

#device = 'cuda' if torch.cuda.is_available() else 'cpu'
device = 'cpu'

def preprocess(text):
    text = re.sub(r'[^a-zA-Z]',' ',text)
    text = ' '.join(text.split())
    return text

def verses(embedder):
    dt = pd.read_csv("../data/texts.csv")
    dt['text'] = dt['content'].apply(preprocess)

    bible=dt.loc[2,'content']
    pattern = r"([a-zA-Z]+) (\d+):(\d+)\t(.+)"

    # Dictionary to hold chapters and verses
    bible_structure = defaultdict(lambda: defaultdict(list))

    # Process the text
    for match in re.finditer(pattern, bible):
        book, chapter, verse, verse_text = match.groups()
        bible_structure[book][int(chapter)].append((int(verse), verse_text.strip()))

    corpus = []
    for book, chapters in bible_structure.items():
        for chapter, verses in sorted(chapters.items()):
            for verse_num, verse_text in sorted(verses):
                corpus.append(verse_text)



    print("creating embeddings...")
    embeddings = embedder.encode(corpus, convert_to_numpy=True)

    embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)

    # Build a FAISS index with inner product (for cosine similarity with normalized vectors)
    embedding_dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(embedding_dim)
    index.add(embeddings)
    print("embeddings saved")
    faiss.write_index(index, "../data/faiss_index.bin")
    with open("../data/corpus.json", "w") as f:
        json.dump(corpus, f)

def format_entry(row):
    return f"""{row['commentary']}"""

def commentaries(embedder):
    df = pd.read_csv("../data/text_with_commentary.csv")
    data = list(df.apply(format_entry, axis=1))

    print("create embeddings...")
    embeddings = embedder.encode(data, convert_to_tensor=True, device = device)
    emb_np = embeddings.cpu().detach().numpy()
    index = faiss.IndexFlatL2(emb_np.shape[1])
    faiss.write_index(index, "../data/comm_index.bin")
    index.add(emb_np)
    with open("../data/comm_corpus.json", "w") as f:
        json.dump(data, f)


verses(embedder)
commentaries(embedder)
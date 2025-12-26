import json
import re
import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import pickle
from tqdm import tqdm  


EMBEDDING_MODEL_NAME = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
INDEX_FILE = "index/faiss_index.bin"
OFFERS_FILE = "index/offers.pkl"
JSON_FILE = "data/offers.json"  
BATCH_SIZE = 32


def strip_html(text):
    """Remove HTML tags from text"""
    if text is None:
        return ""
    clean = re.compile("<.*?>")
    return re.sub(clean, "", text).replace("\n", " ")

def build_search_text(offer):
    """
    Build a single string from all relevant fields to embed.
    """
    text_parts = [
        f"სათაური: {offer.get('title','')}",
        f"ბრენდი: {offer.get('brandNames','')}",
        f"კატეგორია: {offer.get('categoryDesc','')}",
        f"ქალაქი: {offer.get('cityNames','')}",
        f"ბარათი: {offer.get('productCodes','')}",
        f"სარგებელი: {offer.get('shortDesc','')}",
        f"აღწერა: {strip_html(offer.get('longDesc',''))}"
    ]
    return " ".join(text_parts)



def main():
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        offers = json.load(f)
    
    print(f"Loaded {len(offers)} offers")

    search_texts = [build_search_text(o) for o in offers]

    print(f"Loading embedding model: {EMBEDDING_MODEL_NAME}")
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    print("Computing embeddings...")
    embeddings = []
    for i in tqdm(range(0, len(search_texts), BATCH_SIZE), desc="Embedding offers"):
        batch = search_texts[i:i+BATCH_SIZE]
        batch_emb = model.encode(batch, normalize_embeddings=True)
        embeddings.append(batch_emb)

    embeddings = np.vstack(embeddings).astype("float32")


    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    faiss.normalize_L2(embeddings)  
    index.add(embeddings)

    print(f"FAISS index built with {index.ntotal} vectors (dim={dim})")


    os.makedirs("index", exist_ok=True)

    faiss.write_index(index, INDEX_FILE)
    with open(OFFERS_FILE, "wb") as f:
        pickle.dump(offers, f)

    print(f"Saved FAISS index to {INDEX_FILE}")
    print(f"Saved offers data to {OFFERS_FILE}")

if __name__ == "__main__":
    main()

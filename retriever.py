import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from utils import prepare_offer_text

INDEX_FILE = "index/faiss_index.bin"
METADATA_FILE = "index/offers.pkl"
EMBEDDING_MODEL_NAME = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"

class OfferRetriever:
    def __init__(self):

        with open(METADATA_FILE, "rb") as f:
            self.offers = pickle.load(f)


        self.index = faiss.read_index(INDEX_FILE)

        self.model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    def search(self, query, top_k=5):
        q_vec = self.model.encode([query], normalize_embeddings=True)
        q_vec = np.array(q_vec).astype("float32")
        faiss.normalize_L2(q_vec)

        scores, idxs = self.index.search(q_vec, top_k)
        results = [self.offers[i] for i in idxs[0]]
        return results

    def prepare_context(self, query, top_k=5):

        results = self.search(query, top_k)
        texts = [prepare_offer_text(o) for o in results]
        context = "\n\n".join(texts)
        return context

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')


def _normalize(vectors: np.ndarray) -> np.ndarray:
    """L2-normalize so that inner-product == cosine similarity."""
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    norms = np.where(norms == 0, 1, norms)   # avoid div-by-zero
    return vectors / norms


def create_index(text_chunks):
    embeddings = model.encode(text_chunks).astype('float32')
    embeddings = _normalize(embeddings)
    dimension = embeddings.shape[1]
    # IndexFlatIP with normalized vectors == cosine similarity
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)
    return index, embeddings


def query_index(query, index, chunks, k=3):
    query_vector = model.encode([query]).astype('float32')
    query_vector = _normalize(query_vector)
    k = min(k, len(chunks))   # guard against fewer chunks than k
    scores, indices = index.search(query_vector, k)
    return [chunks[i] for i in indices[0]]
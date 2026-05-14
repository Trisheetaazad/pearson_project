import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def create_index(text_chunks):
    embeddings = model.encode(text_chunks)
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings).astype('float32'))
    return index, embeddings

def query_index(query, index, chunks, k=3):
    query_vector = model.encode([query])
    distances, indices = index.search(np.array(query_vector).astype('float32'), k)
    return [chunks[i] for i in indices[0]]
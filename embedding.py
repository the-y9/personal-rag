from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from sklearn.preprocessing import normalize
import pickle
from chunking import all_chunks, documents
import time

start = time.time()
# Load Sentence Transformer model
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')


# Generate embeddings and normalize
embeddings = model.encode(all_chunks)
embeddings = normalize(embeddings)

# FAISS Index
embedding_dim = embeddings.shape[1]
index = faiss.IndexFlatL2(embedding_dim)
index.add(np.array(embeddings, dtype=np.float32))

# Save index and metadata
faiss.write_index(index, 'faiss_index.index')
with open('documents.pkl', 'wb') as f:
    pickle.dump(documents, f)

end = time.time()
print(f"Indexing time: {end - start:.2f} seconds")

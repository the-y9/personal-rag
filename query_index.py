from embedding import model, normalize, index, documents
import numpy as np

# Search function
def search(query, k=3):
    query_embedding = model.encode([query])
    query_embedding = normalize(query_embedding)
    _, indices = index.search(np.array(query_embedding, dtype=np.float32), k)
    return [documents[idx] for idx in indices[0]]

if __name__ == "__main__":
    try:
        query = "Are you a developer?"
        results = search(query)
        print(f"top {len(results)} docs")
        for doc in results:
            print(f"Source: {doc['source']}")
            print(f"Text: {doc['text'][:200]}...\n{'-'*40}")
    except Exception as e:
        print(f"An error occurred: {e}")

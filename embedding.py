from sentence_transformers import SentenceTransformer
import mistune
import json
import faiss
import numpy as np
from sklearn.preprocessing import normalize
import pickle

# Load Sentence Transformer model
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Markdown file processor using mistune
def process_markdown(file_path):
    markdown = mistune.create_markdown()
    with open(file_path, 'r') as file:
        markdown_text = file.read()
    return markdown(markdown_text)

# JSON file processor
def process_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        return json.dumps(data)

# Load and process files
aiml_text = process_markdown('data/cover_letter/aiml.md')
dsai_text = process_markdown('data/resume/dsai.md')
skills_text = process_json('data/skills.json')
project_text = process_json('data/project.json')

# Combine all documents for embedding
texts = [aiml_text, dsai_text, skills_text, project_text]

# Generate and normalize embeddings
embeddings = model.encode(texts)
embeddings = normalize(embeddings)

# Create FAISS index
embedding_dim = embeddings.shape[1]
index = faiss.IndexFlatL2(embedding_dim)
index.add(np.array(embeddings, dtype=np.float32))

# Store metadata for retrieval
documents = [
    {"text": aiml_text, "source": "aiml.md"},
    {"text": dsai_text, "source": "dsai.md"},
    {"text": skills_text, "source": "skills.json"},
    {"text": project_text, "source": "project.json"}
]

# Save FAISS index
faiss.write_index(index, 'faiss_index.index')

# Save metadata
with open('documents.pkl', 'wb') as f:
    pickle.dump(documents, f)


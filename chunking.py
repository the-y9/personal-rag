# import mistune
import os
import json

def chunk_text(text, chunk_size=60, overlap=None):
    if overlap is None:
        overlap = chunk_size // 6

    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i+chunk_size])
        chunks.append(chunk)

    return chunks

def process_markdown_chunks(file_path):
    # markdown = mistune.create_markdown()
    with open(file_path, 'r') as file:
        markdown_text = file.read()
    # plain_text = markdown(markdown_text)
    return chunk_text(markdown_text)

def process_json_chunks(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        json_str = json.dumps(data)
    return chunk_text(json_str)

# Chunked text from files
aiml_chunks = process_markdown_chunks('data/cover_letter/aiml.md')
dsai_chunks = process_markdown_chunks('data/resume/dsai.md')
skills_chunks = process_json_chunks('data/skills.json')
project_chunks = process_json_chunks('data/project.json')

all_chunks = aiml_chunks + dsai_chunks + skills_chunks + project_chunks

# Metadata for each chunk
documents = []

# Track sources for each chunk
sources = (
    ['aiml.md'] * len(aiml_chunks) +
    ['dsai.md'] * len(dsai_chunks) +
    ['skills.json'] * len(skills_chunks) +
    ['project.json'] * len(project_chunks)
)

# Add metadata
for chunk, src in zip(all_chunks, sources):
    documents.append({'text': chunk, 'source': src})


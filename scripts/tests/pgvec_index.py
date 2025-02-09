"""
This script is used to index the documents into the vector database.
PGVector looks a lot slower than Chroma, that's why we're using Chroma for now and leaving this here for reference.
"""
import os
import vecs
from openai import OpenAI
from vecs.adapter import Adapter, ParagraphChunker, TextEmbedding

database_url = os.getenv("DATABASE_URL")
vx = vecs.create_client(database_url)
client = OpenAI()
docs = vx.get_or_create_collection(
    name="docs",
    adapter=Adapter(
        [
            TextEmbedding(model='all-MiniLM-L6-v2'),
        ]
    )
)


def embed_text(text: str):
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=text,
        encoding_format="float"
    )
    return response.data[0].embedding


from pathlib import Path
import re
from typing import List
from dataclasses import dataclass

@dataclass
class DocChunk:
    """Represents a document chunk with its metadata."""
    topic: str
    title: str
    content: str
    description: str = ""

def extract_doc_chunks(content: str,topic: str) -> List[DocChunk]:
    """
    Extract document chunks from content by finding <doc> tags using regex.
    
    Args:
        content (str): The content to parse
        
    Returns:
        List[DocChunk]: List of document chunks with their metadata
    """
    chunks = []
    
    # Pattern to match <doc title="..." desc="...">content</doc>
    pattern = r'<doc\s+title="([^"]*)"\s*(?:desc="([^"]*)")?\s*>(.*?)</doc>'
    
    # Find all matches
    matches = re.finditer(pattern, content, re.DOTALL)
    
    for match in matches:
        title = match.group(1)
        description = match.group(2) if match.group(2) else ""
        content = match.group(3).strip()
        
        chunk = DocChunk(
            topic=topic,
            title=title,
            description=description,
            content=content
        )
        chunks.append(chunk)
    
    return chunks

def read_and_chunk_docs(file_path: str) -> List[DocChunk]:
    """
    Read a file and extract document chunks from it.
    
    Args:
        file_path (str): Path to the file to read
        
    Returns:
        List[DocChunk]: List of document chunks
    """
    try:
        # Extract topic from the content path
        topic = file_path.split("/")[-1].split(".")[0]
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        chunks = extract_doc_chunks(content,topic)
        return chunks
    except Exception as e:
        print(f"Error reading file {file_path}: {str(e)}")
        return []

# Example usage:
def add_docs():
    records = []
    # Test with MonsterUI context
    doc_paths = [".llms/MonsterUI-ctx.txt",".llms/FastHTML.txt"]
    for doc_path in doc_paths:
        chunks = read_and_chunk_docs(doc_path)
        for chunk in chunks:
            print(f"Processing: {chunk.topic} - {chunk.title}")
            records.append((chunk.topic+"-"+chunk.title,chunk.content.strip(),{"topic":chunk.topic,"content":chunk.content,"description":chunk.description}))
    docs.upsert(records=records)
    print("Documents added to database")

if __name__ == "__main__":
    # add_docs()
    # search by text
    query = "Create a blog card with a title, description, and image"
    results = docs.query(data=query,measure="cosine_distance",limit=1, include_value=False,include_metadata=True)
    for result in results:
        print("TOPIC:",result[0])
        print("CONTENT:",result[1]["content"][:100])

    
    
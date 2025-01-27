import chromadb
import re
from typing import List
from dataclasses import dataclass
import json

client = chromadb.PersistentClient()

collection = client.get_or_create_collection(name="docs")

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
    doc_paths = [".llms/MonsterUI-ctx.txt",".llms/FastHTML.txt"]
    for doc_path in doc_paths:
        chunks = read_and_chunk_docs(doc_path)
        for chunk in chunks:
            print(f"Processing: {chunk.topic} - {chunk.title}")
            records.append((chunk.topic+"-"+chunk.title,chunk.content.strip(),{"topic":chunk.topic,"content":chunk.content,"description":chunk.description}))
    documents = [record[1] for record in records]
    idxs = [record[0] for record in records]
    metadatas = [record[2] for record in records]
    collection.add(documents=documents,ids=idxs,metadatas=metadatas)

    print("Documents added to database")

def search_docs(query: str):
    results = collection.query(
        query_texts=[query],
        n_results=2
    )
    for metas in results.get("metadatas"):
        for meta in metas:
            print(meta.get("topic"))
            print(meta.get("content")[:100])


if __name__ == "__main__":
    # print("Adding docs")
    # add_docs()
    print("Searching docs")
    search_docs("Create a blog card with a title, description, and image")
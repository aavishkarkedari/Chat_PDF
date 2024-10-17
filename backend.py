# backend.py

import pinecone
import PyPDF2
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import os
from pinecone import Pinecone, ServerlessSpec

# Initialize Pinecone using your API key

def initialize_pinecone(api_key, index_name):
    # Initialize Pinecone using the updated method
    pc = Pinecone(
        api_key="d79317b9-680b-4166-8bb4-4cb913892719"  # Replace with your actual API key
    )

    # Check if the index exists, and create if it doesn't
    index_name = "langchain-chatbot"
    index = pc.Index(index_name)
    # Return the Pinecone instance and index
    return index


# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ''
    for page_num in range(len(reader.pages)):
        text += reader.pages[page_num].extract_text()
    return text


# Function to split document into chunks
def split_docs(documents, chunk_size=500, chunk_overlap=20):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    docs = text_splitter.split_documents([Document(page_content=documents)])
    return docs


# Function to generate embeddings
def generate_embeddings(docs, model_name="all-MiniLM-L6-v2"):
    embeddings = SentenceTransformerEmbeddings(model_name=model_name)
    doc_texts = [doc.page_content for doc in docs]
    doc_embeddings = embeddings.embed_documents(doc_texts)
    return doc_embeddings


# Function to store embeddings in Pinecone
def store_embeddings_in_pinecone(index, doc_embeddings, docs):
    metadata = [{"id": str(i), "text": doc.page_content} for i, doc in enumerate(docs)]
    vectors = [(str(i), doc_embeddings[i], metadata[i]) for i in range(len(doc_embeddings))]

    # Insert into Pinecone in batches
    def batch_vectors(vectors, batch_size=100):
        for i in range(0, len(vectors), batch_size):
            yield vectors[i:i + batch_size]

    for batch in batch_vectors(vectors, batch_size=100):
        index.upsert(vectors=batch)

    return len(vectors)


# Function to perform a similarity search in Pinecone
def search_similar_docs(index, query_embedding, k=5):
    return index.query(vector=query_embedding, top_k=k, include_metadata=True)
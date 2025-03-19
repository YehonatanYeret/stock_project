import logging
import os

import numpy as np
import pdfplumber
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Distance, VectorParams

# docker run -d --name qdrant -p 6333:6333 qdrant/qdrant
#

# Constants
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
COLLECTION_NAME = "pdf_vectors2"
EMBEDDING_DIM = 2048
PDF_PATH = "MI_PDF_Economic_Dynamics_2025_10_Key_Trends_and_Forecasts.pdf"
TOP_K = 5  # Number of top results to retrieve

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Initialize Qdrant client
client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)


def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def split_text(text, chunk_size=1500, chunk_overlap=150):
    """Splits text into manageable chunks for embedding."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return text_splitter.split_text(text)


def store_embeddings(chunks, embeddings_model):
    """Stores text embeddings in Qdrant."""
    if client.collection_exists(COLLECTION_NAME):
        logging.info("Collection already exists. Skipping embedding storage.")
        return

    logging.info("Creating Qdrant collection...")
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=EMBEDDING_DIM, distance=Distance.COSINE),
    )

    logging.info("Computing embeddings and storing in Qdrant...")
    points = []
    for i, chunk in enumerate(chunks):
        vector = embeddings_model.embed_query(chunk)
        points.append(PointStruct(id=i, vector=vector, payload={"text": chunk}))

    client.upsert(collection_name=COLLECTION_NAME, points=points)
    logging.info("Embeddings stored successfully.")


def search_similar_text(query, embeddings_model, top_k=TOP_K):
    """Searches for the most relevant text chunks in Qdrant."""
    query_vector = embeddings_model.embed_query(query)
    search_results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=top_k
    )
    return [hit.payload["text"] for hit in search_results]


def answer_query(query, model, embeddings_model):
    """Retrieves relevant context and generates an answer using the LLM."""
    context = search_similar_text(query, embeddings_model)
    context_text = "\n".join(context)
    prompt = f"Context:\n{context_text}\n\nQuestion: {query}\nAnswer:"
    return model.invoke(prompt)


if __name__ == "__main__":
    # Initialize embeddings and LLM model
    embeddings_model = OllamaEmbeddings(model="gemma:2b")
    llm = OllamaLLM(model="gemma:2b")

    # Extract and process text
    if not client.collection_exists(COLLECTION_NAME):
        logging.info("Processing PDF...")
        text = extract_text_from_pdf(PDF_PATH)
        chunks = split_text(text)
        store_embeddings(chunks, embeddings_model)
    else:
        logging.info("Embeddings already exist. Skipping PDF processing.")

    # Run a sample query
    query = "Why are national inflation dynamics expected to diverge in 2025? What are the key drivers? answer in 1 short paragraph"
    response = answer_query(query, llm, embeddings_model)
    logging.info(f"Model response: {response}")

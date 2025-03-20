import json
import os
import time

import pdfplumber
import requests
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Constants
PDF_PATH = "MI_PDF_Economic_Dynamics_2025_10_Key_Trends_and_Forecasts.pdf"
API_BASE_URL = "http://localhost:5039/api/queries/PdfEmbedding"  # Update to match your ASP.NET server port
CHUNK_SIZE = 1500
CHUNK_OVERLAP = 150


def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    print(f"Extracting text from: {pdf_path}")
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        for i, page in enumerate(pdf.pages):
            print(f"Processing page {i + 1}/{total_pages}...", end="\r")
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    print(f"\nExtracted {len(text)} characters from {total_pages} pages")
    return text


def split_text(text, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP):
    """Split text into manageable chunks."""
    print(f"Splitting text into chunks (size={chunk_size}, overlap={chunk_overlap})...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = text_splitter.split_text(text)
    print(f"Text split into {len(chunks)} chunks")
    return chunks


def process_pdf():
    """Process the PDF and store embeddings through the API."""
    url = f"{API_BASE_URL}/process-pdf"
    headers = {"Content-Type": "application/json"}

    print(f"Sending process-pdf request to {url}...")
    start_time = time.time()

    response = requests.post(url, headers=headers)

    if response.status_code == 200:
        elapsed_time = time.time() - start_time
        print(f"PDF processed successfully in {elapsed_time:.2f} seconds")
        return True
    else:
        print(f"Error processing PDF: {response.status_code}")
        print(f"Response: {response.text}")
        return False


def query_model(question):
    """Send a query to the API and return the model's answer."""

    url = f"{API_BASE_URL}/process-pdf"
    requests.post(url)

    url = f"{API_BASE_URL}/answer"
    params = {"query": question}

    print(f"Sending query: '{question}'")
    start_time = time.time()

    response = requests.get(url, params=params)

    if response.status_code == 200:
        elapsed_time = time.time() - start_time
        result = response.json()
        print(f"Query processed in {elapsed_time:.2f} seconds")

        # The C# API returns a JSON object with an "answer" field
        if isinstance(result, dict) and "answer" in result:
            return result.get("answer")
        return result
    else:
        print(f"Error querying model: {response.status_code}")
        print(f"Response: {response.text}")
        return None


def local_process_and_store():
    """Process the PDF locally and then store it through the API."""
    # Extract text from PDF locally
    text = extract_text_from_pdf(PDF_PATH)

    # Split text into chunks locally
    chunks = split_text(text)

    # At this point, you would need to implement a custom endpoint in your C# API
    # to accept these chunks, but for now, we'll just use the existing process-pdf endpoint
    print("Note: Your C# API doesn't have a specific endpoint to accept chunks directly.")
    print("Using the process-pdf endpoint instead, which will read the PDF file directly.")

    return process_pdf()


def main():
    print("=" * 50)
    print("PDF Processing and Query Client")
    print("=" * 50)

    # Option 1: Let the server handle everything (recommended)
    # success = process_pdf
    # success =True

    # Option 2: Process locally and send to server (would require API modification)
    # Uncomment the following line if you modify your C# API to accept chunks
    # success = local_process_and_store()
    success = True
    if success:
        # Query examples
        questions = [
            "Why are national inflation dynamics expected to diverge in 2025? What are the key drivers?",
            "What are the 3 main economic trends for 2025?"
        ]

        for question in questions:
            print("\n" + "=" * 50)
            answer = query_model(question)

            print("\nQuestion:")
            print(question)
            print("\nAnswer:")
            print(answer if answer else "No answer received")

    print("\n" + "=" * 50)
    print("Process completed")


if __name__ == "__main__":
    main()

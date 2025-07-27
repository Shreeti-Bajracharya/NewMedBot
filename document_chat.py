import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer
import faiss
import google.generativeai as genai
import os

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
chat_model = genai.GenerativeModel("gemini-2.5-pro")

# Extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

# Create FAISS vector store
def create_vector_store(text):
    model_embed = SentenceTransformer("all-MiniLM-L6-v2")
    chunks = text.split("\n\n")  # Simple paragraph-based split
    embeddings = model_embed.encode(chunks)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    return index, chunks

# Retrieve relevant context + Gemini response
def query_with_context(query, index, chunks, top_k=3):
    model_embed = SentenceTransformer("all-MiniLM-L6-v2")
    query_embedding = model_embed.encode([query])
    D, I = index.search(query_embedding, top_k)
    relevant_chunks = [chunks[i] for i in I[0]]
    context = "\n".join(relevant_chunks)
    prompt = f"{context}\n\nUser: {query}\nAI:"
    response = chat_model.generate_content(prompt)
    return response.text

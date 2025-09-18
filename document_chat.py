# import fitz  # PyMuPDF
# from sentence_transformers import SentenceTransformer
# import faiss
# import google.generativeai as genai
# import os

# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
# chat_model = genai.GenerativeModel("gemini-2.5-pro")

# def extract_text_from_pdf(pdf_path):
#     """
#     Extracts all text from a PDF file.
#     """
#     text = ""
#     with fitz.open(pdf_path) as doc:
#         for page in doc:
#             text += page.get_text()
#     return text

# def create_vector_store(text):
#     """
#     Splits text into chunks, embeds them, and stores in a FAISS index.
#     """
#     model_embed = SentenceTransformer("all-MiniLM-L6-v2")
#     chunks = text.split("\n\n")  
#     embeddings = model_embed.encode(chunks)
#     dim = embeddings.shape[1]

#     index = faiss.IndexFlatL2(dim)
#     index.add(embeddings)
#     return index, chunks

# def query_with_context(query, index, chunks, top_k=3):
#     """
#     Finds top-k relevant chunks from the FAISS index and queries Gemini LLM.
#     """
#     model_embed = SentenceTransformer("all-MiniLM-L6-v2")
#     query_embedding = model_embed.encode([query])

#     D, I = index.search(query_embedding, top_k)
#     relevant_chunks = [chunks[i] for i in I[0]]

#     context = "\n".join(relevant_chunks)
#     prompt = f"{context}\n\nUser: {query}\nAI:"

#     response = chat_model.generate_content(prompt)
#     return response.text

#WITH MONGODB

# from sentence_transformers import SentenceTransformer
# import faiss
# import google.generativeai as genai
# import os

# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
# chat_model = genai.GenerativeModel("gemini-2.5-pro")

# def create_vector_store(docs):
#     """
#     docs: list of strings (each row from CSV)
#     """
#     model_embed = SentenceTransformer("all-MiniLM-L6-v2")
#     chunks = docs  
#     embeddings = model_embed.encode(chunks)
#     dim = embeddings.shape[1]
#     index = faiss.IndexFlatL2(dim)
#     index.add(embeddings)
#     return index, chunks

# def query_with_context(query, index, chunks, top_k=3):
#     model_embed = SentenceTransformer("all-MiniLM-L6-v2")
#     query_embedding = model_embed.encode([query])
#     D, I = index.search(query_embedding, top_k)
#     relevant_chunks = [chunks[i] for i in I[0]]
#     context = "\n".join(relevant_chunks)
#     prompt = f"{context}\n\nUser: {query}\nAI:"
#     response = chat_model.generate_content(prompt)
#     return response.text

#############
import os
import ast
from collections import Counter

from sentence_transformers import SentenceTransformer
import faiss
import google.generativeai as genai
from pymongo import MongoClient
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
chat_model = genai.GenerativeModel("gemini-2.5-pro")

MONGO_URI = "mongodb+srv://shrbaj23_db_user:qdZMAT5HJWdmjzMH@cluster0.a1wephx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client["medical_chat"]
collection = db["documents"]


def load_dataset_from_mongo():
    data_docs = list(collection.find({}))
    if not data_docs:
        return [], []

    texts, labels = [], []

    for doc in data_docs:
        try:
            content_dict = ast.literal_eval(doc["content"])
            texts.append(content_dict["Text"])
            labels.append(content_dict["Label"])
        except Exception as e:
            print(f"Skipping document due to parsing error: {e}")

    def map_label_to_severity(label):
        label = label.lower()
        if label in ["normal"]:
            return "Mild"
        elif label in ["moderate"]:
            return "Moderate"
        else:
            return "Severe"

    severities = [map_label_to_severity(label) for label in labels]

    return texts, severities


def create_vector_store(texts):
    model_embed = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model_embed.encode(texts)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    return index, embeddings


def query_with_context(user_input, index, texts, severities, top_k=3):
    model_embed = SentenceTransformer("all-MiniLM-L6-v2")
    query_embedding = model_embed.encode([user_input])
    D, I = index.search(query_embedding, top_k)

    relevant_texts = [texts[i] for i in I[0]]
    relevant_severities = [severities[i] for i in I[0]]

  
    severity_count = Counter(relevant_severities)
    majority_severity = severity_count.most_common(1)[0][0]

    prompt = f"""
User described symptoms: {user_input}

Based on similar patient cases: {', '.join(relevant_texts)}

Severity: {majority_severity}

Provide response:
- For Mild/Moderate: suggest tips/tricks for self-care
- For Severe: recommend professional mental health consultation
Answer in a friendly, supportive tone.
"""
    response = chat_model.generate_content(prompt)
    return response.text, majority_severity


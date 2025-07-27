from flask import Flask, render_template, request
from dotenv import load_dotenv
import os

from document_chat import extract_text_from_pdf, create_vector_store, query_with_context

app = Flask(__name__)

# Load API key
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Path to PDF
pdf_path = os.path.join("Data", "Short_Medical_PDF.pdf")
index, chunks = None, None

# Load & embed the PDF at startup
if os.path.exists(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    index, chunks = create_vector_store(text)
    print("✅ PDF loaded and embedded")
else:
    print("❌ PDF not found at:", pdf_path)

# Render chat UI
@app.route("/")
def index_page():
    return render_template("chat.html")

# Handle user message
@app.route("/get", methods=["POST"])
def get_bot_response():
    user_msg = request.form["msg"]
    if not index:
        return "Error: PDF not loaded."
    answer = query_with_context(user_msg, index, chunks)
    return str(answer)

if __name__ == "__main__":
    app.run(debug=True, port=8080)

# from flask import Flask, render_template, request
# from dotenv import load_dotenv
# import os
# from document_chat import extract_text_from_pdf, create_vector_store, query_with_context


# app = Flask(__name__)

# load_dotenv()
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# pdf_path = os.path.join("Data", "Short_Medical_PDF.pdf")
# index, chunks = None, None

# if os.path.exists(pdf_path):
#     text = extract_text_from_pdf(pdf_path)
#     index, chunks = create_vector_store(text)
#     print("✅ PDF loaded and embedded")
# else:
#     print("❌ PDF not found at:", pdf_path)


# @app.route("/")
# def index_page():
#     return render_template("chat.html")

# @app.route("/get", methods=["POST"])
# def get_bot_response():
#     user_msg = request.form["msg"]
#     if not index:
#         return "Error: PDF not loaded."
    
#     answer = query_with_context(user_msg, index, chunks)
#     return str(answer)


# if __name__ == "__main__":
#     app.run(debug=True, port=8080)

#WITH MONGODB

# from flask import Flask, render_template, request
# from dotenv import load_dotenv
# import os
# from pymongo import MongoClient

# from document_chat import create_vector_store, query_with_context

# app = Flask(__name__)

# load_dotenv()
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# MONGO_URI = "mongodb+srv://shrbaj23_db_user:qdZMAT5HJWdmjzMH@cluster0.a1wephx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# client = MongoClient(MONGO_URI)
# db = client["medical_chat"]
# collection = db["documents"]

# docs = [doc["content"] for doc in collection.find()]
# index, chunks = None, None

# if docs:
#     index, chunks = create_vector_store(docs)
#     print("✅ MongoDB dataset loaded and embedded")
# else:
#     print("❌ No documents found in MongoDB")

# @app.route("/")
# def index_page():
#     return render_template("chat.html")

# @app.route("/get", methods=["POST"])
# def get_bot_response():
#     user_msg = request.form["msg"]
#     if not index:
#         return "Error: Dataset not loaded."
#     answer = query_with_context(user_msg, index, chunks)
#     return str(answer)

# if __name__ == "__main__":
#     app.run(debug=True, port=8080)

#############

from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
from document_chat import load_dataset_from_mongo, create_vector_store, query_with_context

app = Flask(__name__)

# Load Gemini API key
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Load MongoDB dataset and build embeddings at startup
docs, severities = load_dataset_from_mongo()
if docs:
    index, embeddings = create_vector_store(docs)
    print("✅ MongoDB dataset loaded and embedded")
else:
    index, embeddings = None, None
    print("❌ No documents found in MongoDB")

# Render chat UI
@app.route("/")
def index_page():
    return render_template("chat.html")

# Handle user message
@app.route("/get", methods=["POST"])
def get_bot_response():
    user_msg = request.form["msg"]
    if not index:
        return "Error: Dataset not loaded."
    
    answer, severity = query_with_context(user_msg, index, docs, severities)
    return f"<b>Severity:</b> {severity}<br><br>{answer}"

if __name__ == "__main__":
    app.run(debug=True, port=8080)

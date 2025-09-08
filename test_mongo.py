from pymongo import MongoClient

# Your MongoDB Atlas connection string
MONGO_URI = "mongodb+srv://shrbaj23_db_user:qdZMAT5HJWdmjzMH@cluster0.a1wephx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Connect to MongoDB
client = MongoClient(MONGO_URI)

# Create (or access) a database called "medical_chat"
db = client["medical_chat"]

# Create (or access) a collection called "documents"
collection = db["documents"]

print("✅ Connected to MongoDB Atlas!")

# Optional: insert a test document
collection.insert_one({"content": "Hello MongoDB!", "metadata": {"source": "test"}})

# Optional: retrieve the test document
doc = collection.find_one({"content": "Hello MongoDB!"})
print("Retrieved:", doc)

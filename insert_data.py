import pandas as pd
from pymongo import MongoClient

# MongoDB connection string
MONGO_URI = "mongodb+srv://shrbaj23_db_user:qdZMAT5HJWdmjzMH@cluster0.a1wephx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)

# Select database and collection
db = client["medical_chat"]
collection = db["documents"]

# Load your CSV
df = pd.read_csv("Clinical Text Data.csv")  # Make sure this file is in the same folder

# Convert each row to a document
records = []
for _, row in df.iterrows():
    record = {
        "content": str(row.to_dict()),  # Store row as text
        "metadata": {"source": "Clinical Text Data.csv"}
    }
    records.append(record)

# Insert into MongoDB
if records:
    collection.insert_many(records)
    print(f"✅ Inserted {len(records)} rows into MongoDB")
else:
    print("❌ No data found in CSV")

from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")

# Select database
db = client["family_relationship_db"]

# Select collections
members_collection = db["members"]
relationships_collection = db["relationships"]

print("MongoDB connected successfully!")
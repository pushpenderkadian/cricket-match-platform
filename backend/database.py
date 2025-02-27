from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["cricket_data"]

matches_collection = db["matches"]
live_collection = db["live"]
scorecard_collection = db["scorecards"]
scorecard_collection.create_index("match_id", unique=True)
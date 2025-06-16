from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["scene_frame_split_db"]

frames_col = db["frames"]
matches_col = db["matches"]

from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from bson import ObjectId

app = Flask(__name__)
CORS(app)

load_dotenv()
MONGO_USERNAME = os.environ.get('MONGO_USERNAME')
MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD')
MONGO_HOST = os.environ.get('MONGO_HOST')
MONGO_PORT = os.environ.get('MONGO_PORT')
MONGO_DB = os.environ.get('MONGO_DB')
MONGO_COLLECTION = os.environ.get('MONGO_COLLECTION')

def connect_mongo():
    client = MongoClient(f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}")
    db = client[MONGO_DB]
    collection = db[MONGO_COLLECTION]
    return collection

def find_blogs_post(collection, category):
    if category == "ALL":
        blogs = collection.find()
        return list(blogs)
    try:
        blogs = collection.find({"category": category})
        return list(blogs)
    except ValueError:
        return None
    

def json_serializable(data):
    for item in data:
        item['_id'] = str(item['_id'])  # Convert ObjectId to string
    return data

@app.route('/blogs', methods=['POST'])
def get_blogs():
    db = connect_mongo()
    category = request.json.get('category')
    blogs_post = find_blogs_post(db, category)
    blogs_post = json_serializable(blogs_post)
    return jsonify(blogs_post)

app.run(host='127.0.0.1', port=5051, debug=True)

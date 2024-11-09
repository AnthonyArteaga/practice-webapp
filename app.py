from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
import os

app = Flask(__name__)

#for mongoDB connection
client = MongoClient("")  #replace with MongoDB URI
db = client["TextsDB"]
collection = db["texts"]

@app.route('/submit', methods=['POST'])
def submit_text():
    data = request.json
    text = data.get("text", "")
    entry = {
        "text": text,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    result = collection.insert_one(entry)
    return jsonify({"id": str(result.inserted_id), "text": text, "timestamp": entry["timestamp"]})

if __name__ == '__main__':
    app.run(debug=True)
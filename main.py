import json
import os
import time
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/")
def home():
    return "Im Alive"

@app.get("/news")
def get_news():
    filename = request.args.get("filename")
    try:
        with open(f"blogs/{filename}.json", "r") as f:
            data = json.load(f)
            return data, 200
    except FileNotFoundError:
        return "File does not exist!", 404 

@app.post("/news")
def make_news():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    try:
        with open(f"blogs/{data['filename']}.json", "w") as f:
            data["timestamp"] = str(round(time.time()))
            json.dump(data, f, indent=4)
            return "", 201
    except FileNotFoundError:
        return "File does not exist!", 404 
    

@app.put("/news")
def edit_news():
    filename = request.args.get("filename")
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    try:
        with open(f"blogs/{filename}.json", "r") as f:
            old_data = json.load(f)
            data["timestamp"] = old_data["timestamp"]
        
        with open(f"blogs/{filename}.json", "w") as f:
            json.dump(data, f, indent=4)
            return "", 204
    except FileNotFoundError:
        return "File does not exist!", 404 

@app.delete("/news")
def delete_news():
    path = "blogs/" + request.args.get("filename") + ".json"
    if os.path.exists(path):
        os.remove(path)
        return "", 202
    else:
        return "File does not exist!", 404 

app.run("0.0.0.0", 4321, True)
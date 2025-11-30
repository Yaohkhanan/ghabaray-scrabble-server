# server.py — Flask-based sync API for Ghabaray Scrabble
# --------------------------------------------
# Run this file with:
#   python server.py
# Then the client game can connect at: http://127.0.0.1:5000

from flask import Flask, request, jsonify
import os
import json
from datetime import datetime

app = Flask(__name__)

# Folder for saving match logs
LOGS_DIR = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

@app.route('/')
def home():
    return jsonify({"message": "✅ Ghabaray Scrabble Sync Server is running."})

@app.route('/upload', methods=['POST'])
def upload_log():
    """Client uploads a match log"""
    data = request.get_json(force=True)
    if not data or "log" not in data:
        return jsonify({"error": "Missing log data"}), 400

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"log_{timestamp}.json"
    filepath = os.path.join(LOGS_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return jsonify({"status": "saved", "filename": filename})

@app.route('/logs', methods=['GET'])
def list_logs():
    """Return list of all saved match logs"""
    files = sorted(os.listdir(LOGS_DIR))
    return jsonify({"logs": files})

@app.route('/logs/<name>', methods=['GET'])
def get_log(name):
    """Download a specific match log"""
    filepath = os.path.join(LOGS_DIR, name)
    if not os.path.exists(filepath):
        return jsonify({"error": "Not found"}), 404
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return jsonify(data)

if __name__ == "__main__":
    print("🚀 Ghabaray Scrabble Sync Server starting at http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)

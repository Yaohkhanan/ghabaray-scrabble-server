from flask import Blueprint, request, jsonify, current_app
import os
import json
from datetime import datetime

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    return jsonify({"message": "✅ Ghabaray Scrabble Sync Server is running."})

@main_bp.route("/upload", methods=["POST"])
def upload_log():
    data = request.get_json(force=True)
    if not data or "log" not in data:
        return jsonify({"error": "Missing log data"}), 400

    logs_dir = current_app.config["LOGS_DIR"]

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"log_{timestamp}.json"
    filepath = os.path.join(logs_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return jsonify({"status": "saved", "filename": filename})

@main_bp.route("/logs", methods=["GET"])
def list_logs():
    logs_dir = current_app.config["LOGS_DIR"]
    files = sorted(os.listdir(logs_dir))
    return jsonify({"logs": files})

@main_bp.route("/logs/<name>", methods=["GET"])
def get_log(name):
    logs_dir = current_app.config["LOGS_DIR"]
    filepath = os.path.join(logs_dir, name)

    if not os.path.exists(filepath):
        return jsonify({"error": "Not found"}), 404

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    return jsonify(data)

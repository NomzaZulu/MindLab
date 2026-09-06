from flask import Flask, jsonify, send_from_directory
import os

app = Flask(__name__)


@app.route("/")
def home():
    return send_from_directory(".", "index.html")


@app.route("/api/health")
def health():
    return jsonify({
        "success": True,
        "message": "MindLab backend is running"
    })


@app.route("/api")
def api_home():
    return jsonify({
        "success": True,
        "message": "MindLab API"
    })

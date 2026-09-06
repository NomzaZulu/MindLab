from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "success": True,
        "message": "MindLab backend is running"
    })


@app.route("/api", methods=["GET"])
def api_home():
    return jsonify({
        "success": True,
        "message": "MindLab API"
    })

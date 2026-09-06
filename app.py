from flask import Flask, jsonify

app = Flask(__name__)


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


@app.route("/")
def home():
    return """
    <h1>MindLab Backend</h1>
    <p>Backend is running.</p>
    """

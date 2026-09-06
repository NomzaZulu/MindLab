from flask import Flask, jsonify, request, send_from_directory
from groq import Groq
import os

app = Flask(__name__)

# Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


# =========================================================
# SERVE MIN DLAB FRONTEND
# =========================================================

@app.route("/")
def home():
    return send_from_directory(".", "index.html")


# =========================================================
# HEALTH CHECK
# =========================================================

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "success": True,
        "message": "MindLab backend is running",
        "service": "MindLab Voice Backend"
    })


# =========================================================
# SPEECH → TEXT
# =========================================================

@app.route("/api/transcribe", methods=["POST"])
def transcribe():

    try:
        # Check audio
        if "audio" not in request.files:
            return jsonify({
                "success": False,
                "error": "No audio file received."
            }), 400

        audio_file = request.files["audio"]

        if not audio_file.filename:
            return jsonify({
                "success": False,
                "error": "Empty audio file."
            }), 400

        # Read audio into memory
        audio_data = audio_file.read()

        if not audio_data:
            return jsonify({
                "success": False,
                "error": "Audio file is empty."
            }), 400

        # Send audio to Groq Whisper
        transcription = client.audio.transcriptions.create(
            file=(
                audio_file.filename,
                audio_data,
                audio_file.content_type or "audio/webm"
            ),
            model="whisper-large-v3-turbo",
            language="en",
            response_format="json",
            temperature=0
        )

        text = transcription.text.strip()

        return jsonify({
            "success": True,
            "text": text
        })

    except Exception as e:

        print("Transcription error:", str(e))

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

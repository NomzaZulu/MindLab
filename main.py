from flask import Flask, jsonify, request, send_from_directory
from groq import Groq
import os

app = Flask(__name__)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


@app.route("/")
def home():
    return send_from_directory(".", "index.html")


@app.route("/api/health")
def health():
    return jsonify({
        "success": True,
        "message": "MindLab backend is running"
    })


@app.route("/api/transcribe", methods=["POST"])
def transcribe():

    try:
        if "audio" not in request.files:
            return jsonify({
                "success": False,
                "error": "No audio file received."
            }), 400

        audio_file = request.files["audio"]

        audio_data = audio_file.read()

        if not audio_data:
            return jsonify({
                "success": False,
                "error": "Audio file is empty."
            }), 400

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

        return jsonify({
            "success": True,
            "text": transcription.text.strip()
        })

    except Exception as e:
        print("Transcription error:", str(e))

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

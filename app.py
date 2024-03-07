from flask import Flask, jsonify, request
import speech_recognition as sr
from helpers import translate


app = Flask(__name__)


@app.route("/")
def index():
    return jsonify({
        "status": {
            "code": 200,
            "message": "Success fetching the API"
        },
        "data": None,
    }), 200


@app.route("/upload", methods=["POST"])
def upload():
    if request.method == "POST":
        file = request.files["voice_note"]
        file_path = "voice_note.wav"
        file.save(file_path)

        # Perform Speech Recognition
        recognizer = sr.Recognizer()
        with sr.AudioFile(file_path) as audio_file:
            audio_data = recognizer.record(audio_file)
            try:
                text = recognizer.recognize_google(
                    audio_data, language="id-ID")
                print(text)
                translation_result = translate(text, "id", "ar")
                print(translation_result)
                return jsonify({
                    "status": {
                        "code": 200,
                        "message": "Success uploading and recognizing the audio file",
                    },
                    "data": {
                        "translation_result": translation_result
                    }
                }), 200
            except sr.UnknownValueError:
                return jsonify({
                    "status": {
                        "code": 400,
                        "message": "Unable to recognize speech"
                    },
                    "data": None
                }), 400
            except sr.RequestError as e:
                return jsonify({
                    "status": {
                        "code": 500,
                        "message": "Speech recognition request failed: {}".format(e)
                    },
                    "data": None
                }), 500


if __name__ == "__main__":
    app.run()

from flask import Flask, jsonify, request
import speech_recognition as sr
from helpers import translate
import easyocr


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


@app.route("/translate", methods=["POST"])
def translate_endpoint():
    if request.method == "POST":
        input_data = request.get_json()
        text = input_data["text"]
        source = input_data["source"]
        target = input_data["target"]

        translation_result = translate(text, source, target)

        return jsonify({
            "status": {
                "code": 200,
                "message": "Success translating text"
            },
            "data": {
                "translation_text": translation_result
            }
        }), 200


@app.route("/upload_image", methods=["POST"])
def upload_image():
    if request.method == "POST":
        if "image" not in request.files:
            return jsonify({
                "status": {
                    "code": 400,
                    "message": "No image file provided"
                },
                "data": None
            }), 400

        image = request.files["image"]
        image_path = "static/uploads/image.jpg"
        image.save(image_path)

        # Perform OCR on the image
        reader = easyocr.Reader(['ar'])  # You can specify languages here
        result = reader.readtext(image_path)

        recognized_text = ' '.join([x[1] for x in result])

        return jsonify({
            "status": {
                "code": 200,
                "message": "Success recognizing text from the image"
            },
            "data": {
                "recognized_text": recognized_text
            }
        }), 200


if __name__ == "__main__":
    app.run()

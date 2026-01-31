from flask import Flask, request, jsonify, send_from_directory
from maria import Maria
from flask_cors import CORS
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, static_folder=BASE_DIR)
CORS(app)
bot = Maria()

@app.route("/")
def index():
    return send_from_directory(BASE_DIR, "index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json["message"]
    response = bot.respond(user_input)
    return jsonify({"reply": response})

if __name__ == "__main__":
    app.run(debug=True)
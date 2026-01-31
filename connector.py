from flask import Flask,request,jsonify
from eliza import Maria


app = Flask(__name__)
bot = Maria()

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json["message"]
    response = bot.respond(user_input)
    return jsonify({"reply": response})

if __name__ == "__main__":
    app.run(debug=True)
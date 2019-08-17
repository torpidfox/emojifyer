from flask import Flask
from flask import request
from text_emojifyer import emojify

app = Flask(__name__)

@app.route("/ping")
def ping():
    return "pong"

@app.route("/api/v1/emojify", methods=['POST'])
def emojify_handler():
    text = request.get_data()
    return emojify(text)

if __name__ == "__main__":
    app.run()

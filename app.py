from flask import Flask, render_template, jsonify, request
from src.chatbot import MediBot
from dotenv import load_dotenv
import warnings
warnings.filterwarnings(
    "ignore",
    category=UserWarning,  # LangChainDeprecationWarning is a subclass of UserWarning
    message=".*LangChain uses pydantic v2 internally.*"
)

app = Flask(__name__)

load_dotenv()
medibot = MediBot()


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    print(input)
    response = medibot.ask(msg)
    print("Response : ", response)
    return str(response)



if __name__ == '__main__':
    app.run(host="0.0.0.0", port= 8080, debug= True)

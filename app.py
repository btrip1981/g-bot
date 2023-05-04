import openai
import os
from flask import Flask, render_template, request, jsonify
from tenacity import retry, stop_after_attempt, wait_fixed
import logging
max_attempts = 3
wait_seconds = 2


app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/", methods=["GET", "POST"])
def home():
    app.logger.debug("Home route accessed")
    return render_template("index.html")

@app.route("/G_bot", methods=["GET", "POST"])
def index():
    app.logger.debug("G_bot route accessed")
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    try:
        response = call_gpt4_api(data["messages"])
        return jsonify(response)
    except Exception as e:
        app.logger.error(f"Error in chat route: {e}")
        return jsonify({"error": "An error occurred while processing your request. Please try again later."}), 500




@retry(stop=stop_after_attempt(max_attempts), wait=wait_fixed(wait_seconds))
def call_gpt4_api(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response['choices'][0]['message']['content'].strip()

# ...
if __name__ == "__main__":
    app.run(debug=True)

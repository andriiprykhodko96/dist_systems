from flask import Flask, request, jsonify
import uuid
import requests

app = Flask(__name__)

logging_service_url = "http://localhost:5001/logging"
messages_service_url = "http://localhost:5002/messages"


def call_to_msg():
    response = requests.get(messages_service_url)
    return response.text


def call_to_logging():
    response = requests.get(logging_service_url)
    return response.text


@app.route("/", methods=['GET', 'POST'])
def handler():
    if request.method == "GET":
        logging_response = call_to_logging()
        messages_response = call_to_msg()
        return jsonify(messages_response, logging_response)

    elif request.method == "POST":
        message = request.form.get('msg')
        id = uuid.uuid4()
        logging_payload = {'id': id, 'msg': message}
        response = requests.post(logging_service_url, data=logging_payload)
        return response.text


if __name__ == "__main__":
    app.run(port=5000)
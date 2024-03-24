import random

import hazelcast
from flask import Flask, request, jsonify
import uuid
import requests

app = Flask(__name__)

messages_service_url = "http://localhost:5004/messages"

def call_to_msg():
    response = requests.get(messages_service_url)
    return response.text


def call_to_logging():
    port = random.randint(5001,5003)
    response = requests.get("http://localhost:{0}/logging".format(port))
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
        port = random.randint(5001, 5003)
        response = requests.post("http://localhost:{0}/logging".format(port) ,data=logging_payload)
        return response.text


if __name__ == "__main__":
    app.run(port=5000)
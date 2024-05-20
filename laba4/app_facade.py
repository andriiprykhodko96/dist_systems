import random
import hazelcast
from flask import Flask, request, jsonify
import uuid
import requests

app = Flask(__name__)

hz = hazelcast.HazelcastClient()
mess_q = hz.get_queue("mq").blocking()

def call_to_msg():
    port = random.randint(5004, 5005)
    response = requests.get("http://localhost:{0}/messages".format(port))
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
        return jsonify(f"From message service:{messages_response}\n", f"From logging service: {logging_response}")


    elif request.method == "POST":
        message = request.form.get('msg')
        id = uuid.uuid4()
        logging_payload = {'id': id, 'msg': message}
        port = random.randint(5001, 5003)
        response = requests.post("http://localhost:{0}/logging".format(port) ,data=logging_payload)
        mess_q.offer(message)
        return response.text


if __name__ == "__main__":
    app.run(port=5000)
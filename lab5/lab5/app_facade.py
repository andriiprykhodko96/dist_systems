import random
import hazelcast
from flask import Flask, request, jsonify
import uuid
import requests
import consul
import json
import consul_conf

app = Flask(__name__)
hz = hazelcast.HazelcastClient()

facade_ms = consul_conf.register_ms('facade-ms', 5000)

hz_config_json = consul_conf.get_kv('hz_configs')
if hz_config_json:
    hz_config = json.loads(hz_config_json)
    print("HZ conf:", hz_config)
else:
    print("SMTH WENT WRONG, CHECK CONFIG")
    exit(1)

mq_config_json = consul_conf.get_kv('mq_configs')
if mq_config_json:
    mq_config = json.loads(mq_config_json)
    print("HZ conf:", mq_config)
else:
    print("SMTH WENT WRONG, CHECK CONFIG")
    exit(1)

mess_q = hz.get_queue(mq_config['queue_name']).blocking()

def call_to_msg():
    port = consul_conf.get_service_address_port('messages-ms')
    msg_url = f"{port}/messages"
    response = requests.get(msg_url)
    return response.text

def call_to_logging():
    port = consul_conf.get_service_address_port('logging-ms')
    log_url = f"{port}/logging"
    response = requests.get(log_url)
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
        port = consul_conf.get_service_address_port('logging-ms')
        log_url = f"{port}/logging"
        response = requests.get(log_url)
        mess_q.offer(message)
        return response.text


if __name__ == "__main__":
    app.run(port=5000)
    input("Press F")
    consul_conf.deregister_ms(facade_ms)
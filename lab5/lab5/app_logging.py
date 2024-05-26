from flask import Flask, request, jsonify
import hazelcast
import subprocess
import argparse
import consul_conf
import json

parser=argparse.ArgumentParser()
parser.add_argument("--port", type=int, required=True)
args = parser.parse_args()

messages_map = {}

p = subprocess.Popen(["hz", "start"])
client = hazelcast.HazelcastClient()

logging_ms = consul_conf.register_ms('logging-ms',args.port)

hz_config_json = consul_conf.get_kv('hz_configs')
if hz_config_json:
    hz_config = json.loads(hz_config_json)
    print("HZ conf:", hz_config)
else:
    print("SMTH WENT WRONG, CHECK CONFIG")
    exit(1)

log_map = client.get_map(hz_config['map_name']).blocking()

app = Flask(__name__)

@app.route("/logging", methods=['POST','GET'])
def logging_service():
    if request.method == "POST":
        id = request.form.get('id')
        message = request.form.get('msg')
        log_map.put(id, message)
        print("Received {} with UUID {}".format(message, id))
        return jsonify({'success': True}), 200

    elif request.method == "GET":
        messages = client.get_map("log_map").blocking()
        return " | ".join(messages.values()), 200

if __name__ == "__main__":
    app.run(port=args.port)
    input("Press F")
    consul_conf.deregister_ms(logging_ms)

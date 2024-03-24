from flask import Flask, request, jsonify
import hazelcast
import subprocess
import argparse

parser=argparse.ArgumentParser()
parser.add_argument("--port", type=int, required=True)
args = parser.parse_args()

app = Flask(__name__)
messages_map = {}

p = subprocess.Popen(["hz", "start"])
client = hazelcast.HazelcastClient()
log_map = client.get_map("log_map")

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
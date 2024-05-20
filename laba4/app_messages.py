from flask import Flask,jsonify
import argparse
import hazelcast

app = Flask(__name__)

parser=argparse.ArgumentParser()
parser.add_argument("--port", type=int, required=True)
args = parser.parse_args()

hz = hazelcast.HazelcastClient()
mess_q = hz.get_queue("mq").blocking()
messages = []

@app.route("/messages", methods=['GET'])
def message_service():
    for i in range(0,5):
        message = mess_q.take()
        print(f"CONSUMED {message}")
        if (i==5):
            break
        messages.append(message)
    return jsonify({f"messages on port {args.port}:":messages})

if __name__ == "__main__":
    app.run(port=args.port)

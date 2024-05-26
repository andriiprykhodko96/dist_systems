import json

from flask import Flask,jsonify
import argparse
import hazelcast
import consul_conf

parser=argparse.ArgumentParser()
parser.add_argument("--port", type=int, required=True)
args = parser.parse_args()

messages_ms = consul_conf.register_ms('messages-ms', args.port)

mq_config_json = consul_conf.get_kv('mq_configs')
if mq_config_json:
    mq_config = json.loads(mq_config_json)
    print("HZ conf:", mq_config)
else:
    print("SMTH WENT WRONG, CHECK CONFIG")
    exit(1)

hz = hazelcast.HazelcastClient()
mess_q = hz.get_queue(mq_config['queue_name']).blocking()
messages = []


app = Flask(__name__)
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
    input("Press F")
    consul_conf.deregister_ms(messages_ms)

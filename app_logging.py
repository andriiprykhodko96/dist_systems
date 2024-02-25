from flask import Flask, request, jsonify

app = Flask(__name__)
messages_map = {}


@app.route("/logging", methods=['POST','GET'])
def logging_service():
    if request.method == "POST":
        id = request.form.get('id')
        message = request.form.get('msg')
        messages_map[id] = message
        print("Received {} with UUID {}".format(message, id))
        return jsonify({'success': True}), 200

    elif request.method == "GET":
        return jsonify({'messages': list(messages_map.values())})


if __name__ == "__main__":
    app.run(port=5001)
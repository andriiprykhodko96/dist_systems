from flask import Flask

app = Flask(__name__)
@app.route("/messages", methods=['GET'])
def message_service():
    return "TO BE DONE"


if __name__ == "__main__":
    app.run(port=5004)

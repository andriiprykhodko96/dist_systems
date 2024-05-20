import requests
import time

# URL endpoint to send the POST request to
url = "http://localhost:5000"

# Payload data to be sent in the request body
for i in range(1,11):
    payload = {
        "msg": "message{0}".format(i)
    }

    response = requests.post(url, data=payload)
    # Check the response status code
    print("Sent message {0}; Status {1}".format(payload, response.status_code))

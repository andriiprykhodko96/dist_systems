import requests

# URL endpoint to send the POST request to
url = "http://localhost:5000"

# Payload data to be sent in the request body
payload = {
    "msg": "message1"
}

response = requests.post(url, data=payload)
# Check the response status code
print(response.status_code)
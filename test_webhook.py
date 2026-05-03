import requests

user_message = "what is Ai tell me in one line?"

request_message = {"message": user_message}

url="http://localhost:5678/webhook-test/c0d5190d-34d8-4fc0-8d94-1df6a3ac094a"

response = requests.post(url, json=request_message)

print("Status Code:", response.status_code)

print("Response Body:", response.json()[0]['output'])
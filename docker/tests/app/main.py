import requests
print("hello world!")

response = requests.get("1.1.1.1")
print(response.status_code)
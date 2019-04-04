import requests

url = "http://127.0.0.1:5000/topic"
data = {
    "md5": "s1s1ws1d2e131dwd2e", 
    "host": "tcp://localhost", 
    "port": "5556"
    }
response = requests.post(url, data)
print(response.text)

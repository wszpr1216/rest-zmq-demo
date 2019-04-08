import requests

server_url = "http://127.0.0.1:5002/points"
server_data = {"start": "1", "final": "50"}
server_response = requests.post(server_url, server_data)
md5_str = server_response.text
print(md5_str)

# md5_str = "43a427c8dfc50ac72ad3c0b3f43db6fe"

client_url = "http://127.0.0.1:5000/topic"
client_data = {"md5": md5_str, "host": "tcp://localhost", "port": "5556"}
client_response = requests.post(client_url, client_data)
print(client_response.text)

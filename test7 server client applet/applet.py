import requests

def post_to_server(server_url, server_data):
    server_response = requests.post(server_url, server_data)
    md5_str = server_response.text
    return md5_str


def post_to_client(client_url, client_data):
    client_response = requests.post(client_url, client_data)
    return client_response.text

server_url = "http://127.0.0.1:5002/points"
client_url = "http://127.0.0.1:5000/topic"

server_data1 = {"start": "3", "final": "50"}
md5_str1 = post_to_server(server_url, server_data1)
client_data1 = {"md5": md5_str1, "host": "tcp://localhost", "port": "5556"}
t = post_to_client(client_url, client_data1)
print(t)

server_data2 = {"start": "1", "final": "50"}
md5_str2 =  post_to_server(server_url, server_data2)
client_data2 = {"md5": md5_str2, "host": "tcp://localhost", "port": "5556"}
t = post_to_client(client_url, client_data2)
print(t)

server_data3 = {"start": "10", "final": "50"}
md5_str3 =  post_to_server(server_url, server_data3)
client_data3 = {"md5": md5_str3, "host": "tcp://localhost", "port": "5556"}
t = post_to_client(client_url, client_data3)
print(t)



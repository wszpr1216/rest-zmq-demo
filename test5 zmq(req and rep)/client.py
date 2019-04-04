import zmq
import requests
from random import randrange
import json

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5556")

list1 = []
for time in range(10):

    data = {}

    http_str = "http://127.0.0.1:5000/" + str(randrange(10000, 100000))
    response = requests.get(http_str)
    zip_filter = response.text + "abc"

    data["code"] = zip_filter
    print("Send request {} .".format(zip_filter))

    socket.send_string(zip_filter)

    message = socket.recv_string()

    data["temp"] = message
    print("Received reply {} .".format(message))

    list1.append(data)

# print(json.dumps(list1))
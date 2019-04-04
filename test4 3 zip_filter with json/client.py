import sys
import zmq
import json
import requests
from random import randrange

#  Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)

print("Collecting updates from weather server...")
socket.connect("tcp://localhost:5556")

# zip_filter = sys.argv[1] if len(sys.argv) > 1 else "10001"

http = "http://127.0.0.1:5000/" + str(randrange(10000, 100000))

response = requests.get(http)
zip_filter = response.text
zip_filter2 = str(int(response.text) + randrange(1, 100))
zip_filter3 = str(int(response.text) - randrange(1, 100))
if isinstance(zip_filter, bytes):
    zip_filter = zip_filter.decode('ascii')
print("response is {} {} {}".format(zip_filter, zip_filter2, zip_filter3))
socket.setsockopt_string(zmq.SUBSCRIBE, zip_filter)
socket.setsockopt_string(zmq.SUBSCRIBE, zip_filter2)
socket.setsockopt_string(zmq.SUBSCRIBE, zip_filter3)

list1 = []
for update_nbr in range(20):
    data = {}
    string = socket.recv_string()
    zipcode, temperature = string.split()
    data["code"] = zipcode
    data["temp"] = temperature
    list1.append(data)

json_str = json.dumps(list1)
print(json_str)

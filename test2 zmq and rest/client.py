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

http = "http://127.0.0.1:5000/" + str(randrange(1, 100000))

response = requests.get(http)
print(response.text)
zip_filter = str(response.text)
if isinstance(zip_filter, bytes):
    zip_filter = zip_filter.decode('ascii')
socket.setsockopt_string(zmq.SUBSCRIBE, zip_filter)

data = {"code": list(), "temp": list()}
for update_nbr in range(5):
    string = socket.recv_string()
    zipcode, temperature = string.split()
    data["code"].append(zipcode)
    data["temp"].append(temperature)

print(data)

# print("Average temperature for zipcode '%s' was %dF" %
#       (zip_filter, total_temp / (update_nbr + 1)))

# Process 5 updates
#total_temp = 0
# for update_nbr in range(5):
#     string = socket.recv_string()
#     zipcode, temperature = string.split()
#     print("%d %s %s" % (total_temp, zipcode, temperature))
#     total_temp += int(temperature)
#
#   Weather update client
#   Connects SUB socket to tcp://localhost:5556
#   Collects weather updates and finds avg temp in zipcode
#

import sys
import zmq
import json

#  Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)

print("Collecting updates from weather server...")
socket.connect("tcp://localhost:5556")

# # Subscribe to zip_filter, default is NYC, 10001
# zip_filter = sys.argv[1] if len(sys.argv) > 1 else "10001"

# # Python 2 - ascii bytes to unicode str
# if isinstance(zip_filter, bytes):
#     zip_filter = zip_filter.decode('ascii')
# socket.setsockopt_string(zmq.SUBSCRIBE, zip_filter)

zip_filter = "10002"
if isinstance(zip_filter, bytes):
     zip_filter = zip_filter.decode('ascii')
socket.setsockopt_string(zmq.SUBSCRIBE, zip_filter)


# Process 5 updates
#total_temp = 0
# for update_nbr in range(5):
#     string = socket.recv_string()
#     zipcode, temperature = string.split()
#     print("%d %s %s" % (total_temp, zipcode, temperature))
#     total_temp += int(temperature)
data =  {"code": list(), "temp": list()}
for update_nbr in range(5):
    string = socket.recv_string()
    zipcode, temperature = string.split()
    data["code"].append(zipcode)
    data["temp"].append(temperature)

print(data)

# print("Average temperature for zipcode '%s' was %dF" %
#       (zip_filter, total_temp / (update_nbr + 1)))

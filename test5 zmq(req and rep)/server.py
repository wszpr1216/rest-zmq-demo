import time
import zmq
from flask import Flask
import threading
from random import randrange

def rest_fun():
    app = Flask(__name__)

    @app.route("/<string:zipcode>")
    def index(zipcode):
        return zipcode
    app.run(debug=True, port=5000)

def zmq_fun():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5556")

    while True:
        message = socket.recv_string()
        print("Received request: {} ".format(message))

        reply = str(randrange(-100, 100)) + "def"

        socket.send_string(reply)

threading.Thread(target=zmq_fun).start()
rest_fun()
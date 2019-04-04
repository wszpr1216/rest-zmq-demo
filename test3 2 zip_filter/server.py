import zmq
from random import randrange
from flask import Flask 
import threading

def rest_fun():
    app = Flask(__name__)

    @app.route("/<string:zipcode>")
    def index(zipcode):
        return zipcode

    app.run(debug=True, port=5000)

def zmq_fun():
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:5556")

    while True:
        zipcode = randrange(1, 100000)
        temperature = randrange(-80, 135)

        socket.send_string("%i %i" % (zipcode, temperature))


t_zmq = threading.Thread(target=zmq_fun)
t_zmq.start()
rest_fun()
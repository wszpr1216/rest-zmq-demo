from flask import Flask, request
import zmq
import threading

topic_list = []

def rest_fun(): 

    app = Flask(__name__)

    @app.route('/topic', methods=['POST'])
    def get_topic():
        if request.method == 'POST':
            topic = request.form['md5']
            if topic not in topic_list:
                topic_list.append(topic)
                host = request.form['host'] + ":" + request.form['port']
                message = connect(host, topic).connect_server_by_zmqSUB()
                print(message)
                return "success"
            else:
                return "failed"

    if __name__ == '__main__':
        app.run(debug=True, port=5000)

def zmq_fun(host, topic):
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect(host)
    
    socket.setsockopt_string(zmq.SUBSCRIBE, topic)

    reply = []

    for i in range(10):
        reply.append(socket.recv_string())

    return reply

# 连接类
class connect():
    def __init__(self, host, topic):
        self.host = host
        self.topic = topic

    # 用zmq订阅模式订阅数据
    def connect_server_by_zmqSUB(self):
        return zmq_fun(self.host, self.topic)

rest_fun()
# zmq_fun("tcp://localhost:5556", "s1s1ws1d2e131dwd2e")
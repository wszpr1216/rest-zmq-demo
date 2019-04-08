from flask import Flask, request
import zmq
import threading

topic_list = []


def rest_fun():

    app = Flask(__name__)

    # 通过POST的参数拿到主题(即'md5')
    @app.route('/topic', methods=['POST'])
    def get_topic():
        if request.method == 'POST':
            topic = request.form['md5']

            if topic not in topic_list:
                topic_list.append(topic)
                host = request.form['host'] + ":" + request.form['port']
                # 实例一个connect对象 调用他的connect_server_by_zmqSUB()函数来通过zmq订阅到server发送的数据
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

    # 设置订阅主题
    socket.setsockopt_string(zmq.SUBSCRIBE, topic)
    print("Start receiving, topic is {}".format(topic))

    reply = []

    for i in range(3):
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
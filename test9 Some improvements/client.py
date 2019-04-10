from flask import Flask, request
import threading
import zmq
from topic import Topic

# topic_list = []
file_path = './data/client_topic.json'
topic_list = Topic(file_path)


def rest_fun():

    app = Flask(__name__)

    # 通过POST的参数拿到主题(即'md5')
    @app.route('/topics', methods=['POST'])
    def get_topic():
        if request.method == 'POST':
            topic = request.form['md5']

            if topic not in topic_list.get_topic_list():
                topic_list.update_top_list(topic)
                host = request.form['host'] + ":" + request.form['port']
                # 实例一个connect对象 调用他的connect_server_by_zmqSUB()函数来通过zmq订阅到server发送的数据
                message = zmq_fun(host, topic)
                # print(message)
                print("获取到的值: \ntopic: {} \ndata: {}".format(
                    message[0]["md5"], message[0]["data"]))
                return "添加topic成功"
            else:
                host = request.form['host'] + ":" + request.form['port']
                # 实例一个connect对象 调用他的connect_server_by_zmqSUB()函数来通过zmq订阅到server发送的数据
                message = zmq_fun(host, topic)
                # print(message)
                print("获取到的值: \ntopic: {} \ndata: {}".format(
                    message[0]["md5"], message[0]["data"]))
                return "已存在的topic"

    if __name__ == '__main__':
        app.run(debug=False, port=5000)


def zmq_fun(host, topic):
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect(host)

    # 设置订阅主题
    socket.setsockopt_string(zmq.SUBSCRIBE, topic)
    print("Start receiving, topic is {}".format(topic))

    string = socket.recv_string()
    md5, data = string.split()

    #return [{"md5": reply[0]["md5"], "data": reply[0]["data"]}]
    return [{"md5": md5, "data": data}]


# 连接类 暂时不用
class connect():
    def __init__(self, host, topic):
        self.host = host
        self.topic = topic

    # 用zmq订阅模式订阅数据
    def connect_server_by_zmqSUB(self):
        return zmq_fun(self.host, self.topic)


rest_fun()
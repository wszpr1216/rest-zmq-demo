from topic_threading import topic_threading
import zmq
from flask import Flask, request
from random import randrange
import hashlib
import threading


class zmq_threading(topic_threading):
    data_list = []
    host_list = [
        "tcp://*:5550", "tcp://*:5551", "tcp://*:5552",
        "tcp://*:5553", "tcp://*:5554", "tcp://*:5555",
        "tcp://*:5556", "tcp://*:5557", "tcp://*:5558",
        "tcp://*:5559"
    ]

    def __init__(self, topic, data):
        # while zmq_threading.host_list == []:
        #     pass
        # else:
        print("正在初始化")
        # topic_threading.lock.acquire()
        self._host = zmq_threading.host_list.pop()
        # topic_threading.lock.release()
        super().__init__(self._host, topic)
        self.__set_data(data)

    @property
    def data(self):
        return self._data

    def __set_data(self, data):
        topic_threading.lock.acquire()
        print("设置data为 %s" % data)
        i = topic_threading.topic_list.index(self._topic)
        zmq_threading.data_list.insert(i, data)
        topic_threading.lock.release()
        self._data = data

    def __del__(self):
        topic_threading.lock.acquire()
        i = topic_threading.__del__(self._topic)
        zmq_threading.data_list.pop(i)
        zmq_threading.host_list.append(self._host)
        topic_threading.lock.release()

    def run(self):
        print("启动zmq成功")
        context = zmq.Context()
        socket = context.socket(zmq.PUB)
        print(self._host)
        socket.bind(self._host)
        while True:
            # for i in range(len(zmq_threading.topic_list)):
            socket.send_string("{} {} ".format(self._topic, self._data))


# 生成md5的函数
def create_md5(start, final, database):
    md5str = str(start).zfill(5) + str(final).zfill(5) + str(database)
    m1 = hashlib.md5()
    m1.update(md5str.encode("utf-8"))
    token = m1.hexdigest()
    return token


# 随机生成数据的函数 模拟从数据库里取数据
def create_random_data(start, final, database):
    return randrange(-100, 100)


api = Flask(__name__)


@api.route('/points', methods=['POST', 'GET'])
def points():
    if request.method == 'POST':
        strat_point = int(request.form['start'])
        final_point = int(request.form['final'])
        database = "database01"
        flag = True

        # 根据两个参数生成一个md5值 用来做zmq接口订阅模式的主题
        md5str = create_md5(strat_point, final_point, database)

        topic_text = zmq_threading.topic_list

        # 如果之前生成过这个主题 就不重新生成数据
        if md5str in topic_text:
            flag = False
        if flag:
            # 随机生成一个数据
            data = create_random_data(strat_point, final_point, database)
            t = zmq_threading(md5str, data)
            t.start()
            return "{} {}".format(md5str, t.host)
        # print(topic_text)
        else:
            return ''


if __name__ == '__main__':
    api.run(debug=False, port=5002)

# zmq1 = zmq_threading("tcp://*:5556", "topic1", "data1")
# zmq2 = zmq_threading("tcp://*:5557", "topic2", "data2")

# zmq1.start()
# zmq2.start()
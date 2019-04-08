import zmq
from flask import Flask, request
import hashlib
from random import randrange
import threading
import time



topic_text = \
    [{
        "md5": "12w912eu1di",
        "data": "12"
    },{
        "md5": "1wefwefweffw",
        "data": "123"
    # }]
    },{
        "md5":"43a427c8dfc50ac72ad3c0b3f43db6fe",
        "data": "123asd"
    }]


def zmq_fun():
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:5556")

    topic_text
    while True:
        topic = get_topic()
        for i in range(len(topic)):
            # 通过zmq不停地发送 主题-数据
            # 把这句注释掉就可以不一直弹数据了
            #print(topic)
            time.sleep(1)
            socket.send_string("{} {}".format(topic[i]["md5"],
                                              topic[i]["data"]))


def rest_fun():

    app = Flask(__name__)
    global topic_text

    # 通过 POST 获取 start、final两个参数
    @app.route('/points', methods=['POST'])
    def get_points():
        print("post")
        if request.method == 'POST':

            strat_point = int(request.form['start'])
            final_point = int(request.form['final'])
            database = "database01"
            flag = True

            # 根据两个参数生成一个md5值 用来做zmq接口订阅模式的主题
            md5str = get_token(strat_point, final_point, database)

            for i in range(len(topic_text)):
                # 如果之前生成过这个主题 就不重新生成数据
                if md5str == topic_text[i]["md5"]:
                    flag = False
                    break
            if flag:
                # 随机生成一个数据
                data = get_data(strat_point, final_point, database)
                # 将 主题-数据 添加到list里 理论上md5是 "md5":"43a427c8dfc50ac72ad3c0b3f43db6fe" 数据随机
                # 问题是这里无法改变全局里的topic_text的值 导致zmq_fun()取到的topic_text还是只有2个
                topic_text.append({"md5": md5str, "data": str(data)})
            # 这里print的值没问题
            print(topic_text)

            return md5str

    if __name__ == '__main__':
        app.run(debug=True, port=5002)


# 生成md5的函数
def get_token(start, final, database):
    md5str = str(start).zfill(5) + str(final).zfill(5) + str(database)
    m1 = hashlib.md5()
    m1.update(md5str.encode("utf-8"))
    token = m1.hexdigest()
    return token


# 随机生成数据的函数 模拟从数据库里取数据
def get_data(start, final, database):
    return randrange(-100, 100)


def get_topic():
    return topic_text


# zmq和flask不能在一个线程里 且flask必须在主线程里
threading.Thread(target=zmq_fun).start()
rest_fun()
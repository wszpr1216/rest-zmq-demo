import zmq
from flask import Flask, request
import hashlib
from random import randrange
import threading
import time
import json


class Topic():
    def __init__(self, file='./data.json', topic_list=[]):
        # self.clear_top_list_cache(file) 
        self.set_topic_list(topic_list, file)


    def get_topic_list(self, file='./data.json'):
        f = open(file, 'r', encoding='utf-8')
        try:
            self.topic_list = json.load(f)
        except json.decoder.JSONDecodeError:
            pass
        finally:
            f.close()
        return self.topic_list

    def set_topic_list(self, temp_list, file='./data.json'):
        self.topic_list = temp_list
        f = open(file, 'w', encoding='utf-8')
        json.dump(self.topic_list, f, ensure_ascii=False)
        f.close()

    def update_top_list(self, add_list, file='./data.json'):
        self.topic_list.append(add_list)
        self.set_topic_list(self.topic_list, file)


    def clear_top_list_cache(self, file='./data.json'):
        f = open(file, 'w')
        '''
        # 清空文件会有bug 原因不明
        # bug : json.decoder.JSONDecodeError: Expecting value:
        f.seek(0)
        f.truncate()
        '''
        f.close()



topic_list = Topic()


def zmq_fun():
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:5556")

    while True:
        topic = topic_list.get_topic_list()
        for i in range(len(topic)):
            # 通过zmq不停地发送 主题-数据
            # 把这句注释掉就可以不一直弹数据了
            #print(topic)
            time.sleep(1)
            socket.send_string("{} {}".format(topic[i]["md5"],
                                              topic[i]["data"]))


def rest_fun():

    app = Flask(__name__)

    # 通过 POST 获取 start、final两个参数
    @app.route('/points', methods=['POST'])
    def get_points():
        if request.method == 'POST':

            strat_point = int(request.form['start'])
            final_point = int(request.form['final'])
            database = "database01"
            flag = True

            # 根据两个参数生成一个md5值 用来做zmq接口订阅模式的主题
            md5str = create_md5(strat_point, final_point, database)

            topic_text = topic_list.get_topic_list()
            for i in range(len(topic_text)):
                # 如果之前生成过这个主题 就不重新生成数据
                if md5str == topic_text[i]["md5"]:
                    flag = False
                    break
            if flag:
                # 随机生成一个数据
                data = create_random_data(strat_point, final_point, database)
                json_str = ({"md5": md5str, "data": str(data)})
                topic_list.update_top_list(json_str)
            print(topic_text)

            return md5str

    if __name__ == '__main__':
        app.run(debug=True, port=5002)


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


# zmq和flask不能在一个线程里 且flask必须在主线程里
threading.Thread(target=zmq_fun).start()
rest_fun()
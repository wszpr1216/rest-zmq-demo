import threading


class topic_threading(threading.Thread):
    lock = threading.Lock()
    topic_list = []

    def __init__(self, host, topic):
        if topic not in topic_threading.topic_list:
            topic_threading.lock.acquire()
            threading.Thread.__init__(self)
            self._set_topic(topic)
            self._host = host
            self._append_topiclist()
            topic_threading.lock.release()
            print("topic初始化完毕")
        else:
            raise Exception("topic已存在")

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, host):
        print("设置host为 %s" % host)
        self._host = host

    @property
    def topic(self):
        return self._topic

    def _set_topic(self, topic):
        print("设置topic为 %s" % topic)
        self._topic = topic

    def _append_topiclist(self):
        string = {"topic": self._topic}
        print("正在向topiclist添加数据: %s" % string)
        #topic_threading.lock.acquire()
        topic_threading.topic_list.append(self._topic)
        #topic_threading.lock.release()

    def run(self):
        print("线程在运行了")

    def __del__(self):
        topic_threading.lock.acquire()
        i = topic_threading.topic_list.index(self._topic)
        topic_threading.topic_list.pop(i)
        topic_threading.lock.release()
        return i
        print("释放了")

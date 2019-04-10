import requests


class post():
    def __init__(self, url, data):
        self.set_url(url)
        self.set_data(data)
        self.message = -1

    def get_url(self):
        return self.url

    def set_url(self, url):
        self.url = url

    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data

    def post_fun(self):
        self.message = requests.post(self.get_url(), self.get_data())
        return self.message

    def get_post_status(self):
        if self.message != -1:
            return self.message.status_code
        else:
            self.post_fun().status_code

    def get_post_text(self):
        if self.message != -1:
            return self.message.text
        else:
            return self.post_fun().text


server_url = "http://127.0.0.1:5002/points"
client_url = "http://127.0.0.1:5000/topics"

server_data1 = {"start": "3", "final": "50"}
postserver1 = post(server_url, server_data1)
md5_str1 = postserver1.get_post_text()

client_data1 = {"md5": md5_str1, "host": "tcp://localhost", "port": "5556"}
postclient1 = post(client_url, client_data1)
t1 = postclient1.get_post_text()
if postclient1.get_post_status() == 200:
    print("post成功, 返回的信息: {}".format(t1))

server_data2 = {"start": "1", "final": "50"}
postserver2 = post(server_url, server_data2)
md5_str2 = postserver2.get_post_text()

client_data2 = {"md5": md5_str2, "host": "tcp://localhost", "port": "5556"}
postclient2 = post(client_url, client_data2)
t2 = postclient2.get_post_text()
if postclient2.get_post_status() == 200:
    print("post成功, 返回的信息: {}".format(t2))

server_data3 = {"start": "10", "final": "50"}
postserver3 = post(server_url, server_data3)
md5_str3 = postserver3.get_post_text()

client_data3 = {"md5": md5_str3, "host": "tcp://localhost", "port": "5556"}
postclient3 = post(client_url, client_data3)
t3 = postclient3.get_post_text()
if postclient3.get_post_status() == 200:
    print("post成功, 返回的信息: {}".format(t3))

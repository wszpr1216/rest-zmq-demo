import requests


class post():
    def __init__(self, url, data):
        self.set_url(url)
        self.set_data(data)
        self.message = -1
        self.post_fun()

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
        # if self.message != -1:
        return self.message.status_code
        # else:
        #     self.post_fun().status_code

    def get_post_text(self):
        # if self.message != -1:
        return self.message.text
        # else:
        #     return self.post_fun().text


server_url = "http://127.0.0.1:5002/points"
client_url = "http://127.0.0.1:5000/topics"
server_data1 = {"start": "3", "final": "50"}


def applet(server_url, server_data):
    server_message = post(server_url, server_data).get_post_text()
    if server_message != '':
        server_message_list = server_message.split()
        topic = server_message_list[0]
        host = server_message_list[1]
        host = host.split("*")
        host = host[0] + "localhost" + host[1]
        client_data = {"topic": topic, "host": host}
        client_post = post(client_url, client_data)

        if client_post.get_post_status() == 200:
            return client_post.get_post_text()
        else:
            return "connecting failed"
    else:
        return "topic已存在"


print(applet(server_url, server_data1))
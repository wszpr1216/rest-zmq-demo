# Flask 端口
# from flask import Flask 

# app = Flask(__name__)

# @app.route("/<string:zipcode>")
# def index(zipcode):
#     return zipcode

# print(123)
# if __name__ == "__main__":
#     app.run(debug=True, port=5000)
# import requests

# response = requests.get("http://127.0.0.1:5000/10001")
# print(response.text)


# 线程
# import threading
# import time

# def a():
#     while True:
#         print("a")
#         time.sleep(2)

# def b():
#     while True:
#         print("b")
#         time.sleep(1)

# t_a = threading.Thread(target=a)
# t_b = threading.Thread(target=b)
# # t_a.start()
# t_b.start()
# a()


# md5生成
# import hashlib
# def get_token():
#     md5str = "1" + "50" + "database01"
#     m1 = hashlib.md5()
#     m1.update(md5str.encode("utf-8"))
#     token = m1.hexdigest()
#     return token

# md5 = get_token()
# print(md5)

# list追加数据
# list1 = [{
#         "md5": "12w912eu1di",
#         "data": "12"
#     },{
#         "md5": "12w912eu1di1212",
#         "data": "12"
#     }]
# md5 = "1"
# data = "2"
# list1.append({"md5": md5, "data": data})
# print(list1)

# md5_temp = "1212"

# for key in range(len(list1)):
#     if md5_temp == list1[key]["md5"]:
#         print(1)

# 在函数中改变list的值
# list1 = [1,2,3]
# def change():
#     def chenge1():
#         list1.append(4)
#     chenge1()

# change()
# print(list1)  
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

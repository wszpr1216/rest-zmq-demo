import zmq

def zmq_fun():
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:5556")

    while True:
        for i in range(len(topic_text)):
            socket.send_string("{} {}".format(topic_text[i]["md5"], topic_text[i]["data"]))

topic_text = \
    [{
        "md5": "12w912eu1di",
        "data": "12"
    },{
        "md5": "1wefwefweffw",
        "data": "123"
    },{
        "md5": "1qewfweru1di",
        "data": "1234"
    },{
        "md5": "1qwerqeri",
        "data": "12345"
    },{
        "md5": "s1s1ws1d2e131dwd2e",
        "data": "123456"
    },{
        "md5": "1asdf1di",
        "data": "1234567"
    },{
        "md5": "12adsfasdfasdfi",
        "data": "12345678"
    },{
        "md5": "1asfdasdfasd1di",
        "data": "1234567890"
    },{
        "md5": "sadfdsfsadfasi",
        "data": "123123"
    },{
        "md5": "asdfadsfasdfsi",
        "data": "1231234"
    }]

zmq_fun()
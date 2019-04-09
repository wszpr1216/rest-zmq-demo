import json


class Topic():
    def __init__(self, file='./data/server_topic.json', topic_list=[]):
        # self.clear_top_list_cache(file)
        self.set_topic_list(topic_list, file)

    def get_topic_list(self, file='./data/server_topic.json'):
        f = open(file, 'r', encoding='utf-8')
        try:
            self.topic_list = json.load(f)
        except json.decoder.JSONDecodeError:
            pass
        finally:
            f.close()
        return self.topic_list

    def set_topic_list(self, temp_list, file='./data/server_topic.json'):
        self.topic_list = temp_list
        f = open(file, 'w', encoding='utf-8')
        json.dump(self.topic_list, f, ensure_ascii=False)
        f.close()

    def update_top_list(self, add_list, file='./data/server_topic.json'):
        self.topic_list.append(add_list)
        self.set_topic_list(self.topic_list, file)

    def clear_top_list_cache(self, file='./data/server_topic.json'):
        f = open(file, 'w')
        '''
        # 清空文件会有bug 原因不明
        # bug : json.decoder.JSONDecodeError: Expecting value:
        '''
        f.seek(0)
        f.truncate()
        f.close()
import json


class Topic():
    def __init__(self, file_path, topic_list=[]):
        self.set_json_path(file_path)
        # self.clear_top_list_cache(file)
        self.set_topic_list(topic_list)
        # print("init success")

    def get_topic_list(self):
        f = open(self.get_json_path(), 'r', encoding='utf-8')
        try:
            self.topic_list = json.load(f)
        except json.decoder.JSONDecodeError:
            pass
        finally:
            f.close()
        # print("get_topic success:", self.topic_list)
        return self.topic_list

    def set_topic_list(self, temp_list):
        self.topic_list = temp_list
        f = open(self.get_json_path(), 'w', encoding='utf-8')
        json.dump(self.topic_list, f, ensure_ascii=False)
        # print("set topic success")
        f.close()

    def update_top_list(self, add_list):
        self.topic_list.append(add_list)
        self.set_topic_list(self.topic_list,)

    def clear_top_list_cache(self):
        f = open(self.get_json_path(), 'w')
        '''
        # 清空文件会有bug 原因不明
        # bug : json.decoder.JSONDecodeError: Expecting value:
        '''
        f.seek(0)
        f.truncate()
        f.close()

    def get_json_path(self):
        return self.file_path

    def set_json_path(self, file_path):
        self.file_path = file_path
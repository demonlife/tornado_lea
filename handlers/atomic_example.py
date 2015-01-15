#encoding: utf8

from models.base_model import DBBaseModel

class IndexDemoData(DBBaseModel):
    def __init__(self):
        pass

    def get_demo_data(self):
        data = self.mysql.get("select * from test")
        return data

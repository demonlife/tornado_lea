#coding:utf8

import tornado

from atomic_example import IndexDemoData

class IndexDemoHandler(tornado.web.RequestHandler):
    def get(self):
        index_data_cls = IndexDemoData()
        data = index_data_cls.get_demo_data()
        if data is None:
            self.write('index demo, data len is: 0')
        else:
            self.write('has data')

handlers = [
    (r'/', IndexDemoHandler),
]

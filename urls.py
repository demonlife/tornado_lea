#encoding:utf-8

#encoding:utf8

from tornado.web import RequestHandler

class ErrorHandler(RequestHandler):
    def get(self):
        self.write('404')

handlers = []
sub_handlers = []
ui_modules = {}

error_handler = [
    #(r'.*',ErrorHandler),
]

from handlers import example
handlers.extend(example.handlers)

from handlers import tornado10k
handlers.extend(tornado10k.handlers)

# 需要放在最后
handlers.extend(error_handler)

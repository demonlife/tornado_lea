#coding:utf-8

import os

from tornado import web
from tornado.httpserver import HTTPServer
import tornado.options
from tornado.options import options

from config import config

class Application(web.Application):
    def __init__(self):
        from urls import handlers, sub_handlers, ui_modules

        # tornaod base setting
        settings = {
            'debug':options.debug,
            'template_path':os.path.join(os.path.dirname(__file__),"templates"),
            'static_path':os.path.join(os.path.dirname(__file__),"static"),
            'xsrf_cookies':options.xsrf_cookies,
            'cookie_secret':options.cookie_secret,
            'ui_modules':ui_modules,
            'autoescape':None,
            'xheaders':True,
        }

        super(Application,self).__init__(handlers,**settings)

        for sub_handler in sub_handlers:
            sub_handler_length = len(sub_handler) / 2
            for i in xrange(sub_handler_length):
                self.add_handlers(sub_handler[i * 2],sub_handler[i * 2 + 1])

def main():
    tornado.options.parse_command_line()
    http_server = HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if '__main__' == __name__:
    main()

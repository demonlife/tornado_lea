#encoding: utf-8

'''
tornaod 异步请求
http://www.dongwm.com/archives/shi-yong-tornadorang-ni-de-qing-qiu-yi-bu-fei-zu-sai/
'''
import time

import tornado
import tornado.web
import tornado.gen
import tornado.concurrent
import tornado.ioloop

# 阻塞实现
'''
class SleepHandler(tornado.web.RequestHandler):
    def get(self):
        time.sleep(5)
        self.write('5s')
'''

#非阻塞实现
'''
# tornado 3.0 之前的写法，需要使用回调方法
class SleepHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        tornado.ioloop.IOLoop.instance().add_timeout(time.time() + 5, callback=self.on_response)
    def on_response(self):
        self.write('5s')
        self.finish()
'''

#非阻塞实现
'''
# tornaod 3.0以后新增了coroutine
class SleepHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        yield tornado.gen.Task(tornado.ioloop.IOLoop.instance().add_timeout, time.time() + 5)
        self.write("5s")
'''

class JustNowHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('just now')

# 异步处理mongo
# 此处使用motor, 一个mogodb出品的支持异步的数据库的python驱动
# 一个motor异步调用就会建立一个mongodb连接
# pymongo是有一个mongodb连接池， 因此在使用时，需要考虑各自的优点
import motor
mongodb = motor.MotorClient('localhost', 27017).test

#import pymongo
#mongodb = pymongo.Connection('localhost', 27017).test

class MongoHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        mongodb.tt.save({"a":1})
        cursor = mongodb.tt.find().sort([('a', -1)])
        while (yield cursor.fetch_next):
            message = cursor.next_object()
            self.write('<li>%s</li>' % message['a'])
        self.write('</ul>')
        self.finish()

    def _on_response(self, message, error):
        print 'on response'
        if error:
            raise tornado.web.HTTPError(500, error)
        elif message:
            for i in message:
                self.write('<li>%s</li>' %i['a'])
            else:
                self.write('</ul>')
                self.finish()

'''
from tornado.concurrent import run_on_executor

# 该并发库在python3中自带，在python2中，需要安装pip install futures
from concurrent.futures import ThreadPoolExecutor

class SleepHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(2)
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        # 如果执行的函数会异步返回值则可以采用如下的调用方式，否则可以直接yield
        res = yield self.sleep()
        self.write('sleep')
        self.flush()

    @run_on_executor
    def sleep(self):
        time.sleep(5)
        return 5
'''

from concurrent.futures import ThreadPoolExecutor
from functools import partial, wraps

EXECUTOR = ThreadPoolExecutor(max_workers=4)

def unblock(f):
    @tornado.web.asynchronous
    @wraps(f)
    def wrapper(*args, **kwargs):
        self = args[0]

        '''
        # 带参数的调用
        def callback(future):
            self.write(future.result())
            self.finish()

        EXECUTOR.submit(
            partial(f, *args, **kwargs)
        ).add_done_callback(
            lambda future: tornado.ioloop.IOLoop.instance().add_callback(
                partial(callback, future)))
        '''

        #不带参数， 调用时也可以返回数据
        def callback():
            self.write('no argument')
            self.finish()

        EXECUTOR.submit(
            partial(f, *args, **kwargs)
        ).add_done_callback(
            lambda future: tornado.ioloop.IOLoop.instance().add_callback(
                partial(callback)))
    return wrapper

class SleepHandler(tornado.web.RequestHandler):
    @unblock
    def get(self, n):
        time.sleep(float(n))
        return "Awake! %s" % time.time()

class SleepAsyncHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self, n):
        def callback(future):
            self.write(future.result())
            self.finish()
        EXECUTOR.submit(
            partial(self.get_, n)
        ).add_done_callback(lambda future: tornado.ioloop.IOLoop.instance().add_callback(
            partial(callback, future)))

    def get_(self, n):
        time.sleep(float(n))
        # 如果不返回数据，程序会报错， 原因是： callback定义中需要数据
        return 'awke'

handlers = [
    (r'/sleep/(\d+)', SleepHandler),
    (r'/sleep', SleepHandler),
    (r'/sleep2/(\d+)', SleepAsyncHandler),
    (r'/just', JustNowHandler),
    (r'/mongo', MongoHandler),
]

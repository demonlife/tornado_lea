#encoding: utf8

from __future__ import absolute_import

import torndb
import redis
import pymongo
from tornado.options import options

from config import config

# mongo with nothing setting
mongo_con = pymongo.Connection('localhost', 27017)
mongo_db = mongo_con.test

#mongo master-slave
'''
mongo_client = 'master.mongodb.idc:27017, slave0.mongodb.idc:27018'
mongo_usr = 'usr'
mongo_pwd = 'pwd'
mongo_repname = 'repset' # 集群名
mongo_db = 'dbname'

# 写连接
wmongo = pymongo.MongoReplicaSetClient(mongo_client,
                                       replicaSet=mongo_repname)
wmongo[mongo_db].authenticate(mongo_user, mongo_pwd)
# 读取连接
rmongo = pymongo.MongoReplicaSetClient(mongo_client,
                                       replicaSet=mongo_repname,
                                       read_preference=pymongo.ReadPreference.SECONDARY)
rmongo[mongo_db].authenticate(mongo_usr, mongo_pwd)
'''

# mysql 连接
mysql_con = torndb.Connection(
    host = options.mysql_host,
    database = options.mysql_database,
    user = options.mysql_user,
    password = options.mysql_password
)

# redis 连接
redis_con = redis.StrictRedis(
    host = options.redis_host,
    port = options.redis_port,
    db = options.redis_db
)

class DBBaseModel(object):
    def __init__(self):
        pass

    @property
    def wmongo(self):
        return mongo_db

    @property
    def rmongo(self):
        return mongo_db

    @property
    def mysql(self):
        return mysql_con

    @property
    def redis(self):
        return redis_con

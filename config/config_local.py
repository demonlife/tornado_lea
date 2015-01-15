#encoding: utf8

from tornado.options import define

define("port",default=10002,help="run on the given port",type=int)
define("mysql_host",default="localhost:3306",help="blog database host")
define("mysql_database",default="wnb_test",help="blog database name")
define("mysql_user",default="test",help="blog database user")
define("mysql_password",default="test",help="blog database password")

define("mongo_client",default="master.mongodb.idc:27017,slave0.mongodb.idc:27018,slave1.mongodb.idc:27019",help="mongodb server")
define("mongo_user",default="chengmi",help="blog database name")
define("mongo_pwd",default="je47dh&8eh)!dfd",help="blog database name")

define("debug",default=True,help="open debug mode")
define("xsrf_cookies",default=True,help="open xsrf cookie")
define("cookie_secret",default="chengmi",help="set cookie secret")
define("WB_KEY",default="3083310234",help="weibo key")
define("WB_SKEY",default="afeae9586c2800870cc93fec005faa46",help="weibo secret key")
define("WB_CALLBACK",default="http://www.chengmi.com/login/sina_callback",help="weibo callback url")

define('redis_port',default=6379,help="run on the give port",type=int)
define('redis_host',default='localhost',help="server host")
define('redis_db',default=14,help="缓存所有的数据，除了session之外的")

define('mongo_host', default='localhost')
define('mongo_port', default=27017, type=int)

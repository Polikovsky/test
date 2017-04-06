import os
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define,options

import pymongo
from pymongo import Connection

MONGODB_HOST="192.168.1.2"
MONGODB_PORT=27017

define("port",default=8888,help="run on the given port",type=int)

class Application(tornado.web.Application):
	def __init__(self):
		handlers=[(r"/",RootHandler),]
		settings=dict()
		tornado.web.Application.__init__(self,handlers,**settings)

		self.connection=pymongo.Connection(MONGODB_HOST,MONGODB_PORT)
		self.db=self.connection["crossmfiters"]

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

class RootHandler(tornado.web.RequestHandler):
    def get(self):
        result=list(self.db.contents.find({},limit=1))
        self.write("I am a greate dev")

def main():
    tornado.options.parse_command_line()
    http_server=tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instanse().start()

if __name__== "__main__":
    main()
    
    
                  

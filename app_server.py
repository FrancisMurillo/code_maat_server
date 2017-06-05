from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from app import app, app_port

server = HTTPServer(WSGIContainer(app))
server.listen(app_port)
IOLoop.instance().start()

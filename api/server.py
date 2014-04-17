import os
import tornado.ioloop
import tornado.web
from model import Users

app_path = os.path.join(os.path.dirname(__file__), "../app")

class UsersHandler(tornado.web.RequestHandler):
    def get(self, id):
        self.write("users" + id)

class FriendsHandler(tornado.web.RequestHandler):
    def get(self, id):
        json_friends = Users.get_friends(id)

        self.write(json_friends)


application = tornado.web.Application([
    (r'/app/(.*)', tornado.web.StaticFileHandler, {'path': app_path}),
    (r"/users/(\d+)", UsersHandler),
    (r"/users/(\d+)/friends", FriendsHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
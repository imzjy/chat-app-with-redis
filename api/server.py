import os
import tornado.ioloop
import tornado.web
from model import Users, Messages

app_path = os.path.join(os.path.dirname(__file__), "../app")

class UsersHandler(tornado.web.RequestHandler):
    def get(self, id):
        self.write("users" + id)

class FriendsHandler(tornado.web.RequestHandler):
    def get(self, id):
        json_friends = Users.get_friends(id)

        self.write(json_friends)

class InMessageHandler(tornado.web.RequestHandler):
    def post(self):
        json_msg = self.request.body
        result = Messages.save(json_msg)
        if result[0] > 0:
            self.write(result[1])
        else:
            pass #TODO:error process

class UnreadsMessageHandler(tornado.web.RequestHandler):
    def get(self, id):
        json_unread_messages = Messages.get_unread(id)
        self.write(json_unread_messages)

application = tornado.web.Application([
    (r'/app/(.*)', tornado.web.StaticFileHandler, {'path': app_path}),
    (r"/users/(\d+)", UsersHandler),
    (r"/users/(\d+)/friends", FriendsHandler),
    (r"/users/(\d+)/messages/unread", UnreadsMessageHandler),
    (r"/message/in", InMessageHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
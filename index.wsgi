import tornado.wsgi
import tornado.web
import sae
import src.handler.route

app = tornado.wsgi.WSGIApplication(src.handler.route.handlers)

application = sae.create_wsgi_app(app)

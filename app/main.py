# -*- coding: utf-8 -*-

import falcon
from falcon_multipart.middleware import MultipartMiddleware


from app import log
from app.middleware import JSONTranslator, DatabaseSessionManager
from app.database import db_session, init_session

from app.api.common import base
from app.api.v1 import dashboard
from app.errors import AppError
from app.utils import HandleCORS

LOG = log.get_logger()

class App(falcon.API):
    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)
        LOG.info("API Server is starting")

        self.add_route("/", base.BaseResource())
        self.add_route("/v1/dashboard/objectives", dashboard.Dashboard())  # GET
        self.add_route("/v1/dashboard/departments", dashboard.Dashboard())  # GET

        self.add_error_handler(AppError, AppError.handle)


init_session()
middleware = [
    JSONTranslator(),
    DatabaseSessionManager(db_session),
    MultipartMiddleware(),HandleCORS() ]
application = App(middleware=middleware)

if __name__ == "__main__":
    from wsgiref import simple_server
    httpd = simple_server.make_server("127.0.0.1", 5000, application)
    httpd.serve_forever()

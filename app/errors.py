# -*- coding: utf-8 -*-

import json
import falcon

try:
    from collections import OrderedDict
except ImportError:
    OrderedDict = dict


OK = {"status": falcon.HTTP_200, "code": 200}

ERR_UNKNOWN = {
    "status": falcon.HTTP_500,
    "code": 500,
    "title": "Unknown Error"}

ERR_AUTH_REQUIRED = {
    "status": falcon.HTTP_401,
    "code": 99,
    "title": "Authentication Required",
}

ERR_INVALID_PARAMETER = {
    "status": falcon.HTTP_400,
    "code": 88,
    "title": "Invalid Parameter",
}

ERR_DATABASE_ROLLBACK = {
    "status": falcon.HTTP_500,
    "code": 77,
    "title": "Database Rollback Error",
}

ERR_NOT_SUPPORTED = {
    "status": falcon.HTTP_404,
    "code": 10,
    "title": "Not Supported"}


ERR_USER_NOT_EXISTS = {
    "status": falcon.HTTP_404,
    "code": 21,
    "title": "User Not Exists",
}


ERR_DUPLICATE_ENTRY = {
    "status": falcon.HTTP_409,
    "code": 409,
    "title": "already exists",
}

ERR_FORBIDEN_ACCESS = {
    "status": falcon.HTTP_200,
    "code": 403,
    "title": "forbiden access",
}

ERR_DB_PRECONDITION_FAILED = {
    "status": falcon.HTTP_412,
    "code": 412,
    "title": "db precondition failed",
}


class AppError(Exception):
    def __init__(self, error=ERR_UNKNOWN, description=None):
        self.error = error
        self.error["description"] = description

    @property
    def code(self):
        return self.error["code"]

    @property
    def title(self):
        return self.error["title"]

    @property
    def status(self):
        return self.error["status"]

    @property
    def description(self):
        return self.error["description"]

    @staticmethod
    def handle(exception, req, res, error=None):
        res.status = exception.status
        meta = OrderedDict()
        meta["code"] = exception.code
        meta["message"] = exception.title
        if exception.description:
            meta["description"] = exception.description
        res.body = json.dumps({"meta": meta})


class InvalidParameterError(AppError):
    def __init__(self, description=None):
        super().__init__(ERR_INVALID_PARAMETER)
        self.error["description"] = description


class DatabaseError(AppError):
    def __init__(self, error, args=None, params=None):
        super().__init__(error)
        obj = OrderedDict()
        obj["details"] = ", ".join(args) if args else ''
        obj["params"] = str(params)
        self.error["description"] = obj


class NotSupportedError(AppError):
    def __init__(self, method=None, url=None):
        super().__init__(ERR_NOT_SUPPORTED)
        if method and url:
            self.error["description"] = "method: %s, url: %s" % (method, url)



class UnauthorizedError(AppError):
    def __init__(self, description=None):
        super().__init__(ERR_AUTH_REQUIRED)
        self.error["description"] = description



class DuplicateEntryError(AppError):
    def __init__(self, description=None):
        super().__init__(ERR_DUPLICATE_ENTRY)
        self.error["description"] = description


class DatabasePreConditionError(AppError):
    def __init__(self, description=None):
        super().__init__(ERR_DB_PRECONDITION_FAILED)
        self.error["description"] = description

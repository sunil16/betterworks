# -*- coding: utf-8 -*-

import falcon
import sqlalchemy.orm.scoping as scoping
from sqlalchemy.exc import SQLAlchemyError

from app.log import LOG
from app import config
from app.errors import DatabaseError, ERR_DATABASE_ROLLBACK, InvalidParameterError

# LOG = log.get_logger()

class DatabaseSessionManager(object):
    def __init__(self, db_session):
        self._session_factory = db_session
        self._scoped = isinstance(db_session, scoping.ScopedSession)

    def process_request(self, req, res, resource=None):
        """
        Handle post-processing of the response (after routing).
        """
        LOG.debug("DatabaseSessionManager done")
        req.context["session"] = self._session_factory

    def process_response(self, req, res, resource=None, req_succeeded=None):
        """
        Handle post-processing of the response (after routing).
        """
        try:
            session = req.context["session"]
        except:
            raise InvalidParameterError('empty db session')

        if config.DB_AUTOCOMMIT:
            try:
                session.commit()
            except SQLAlchemyError as ex:
                out = session.rollback()
                reason = ex.args[0]
                LOG.error(reason)
                LOG.error(ex.args)

                sql_detail_index = reason.find('\n\n')
                LOG.debug('index is:{}'.format(sql_detail_index))

                if sql_detail_index != -1:
                    raise DatabaseError(
                        ERR_DATABASE_ROLLBACK, (str(reason[:sql_detail_index]),))
                else:
                    raise DatabaseError(ERR_DATABASE_ROLLBACK)

        if self._scoped:
            # remove any database-loaded state from all current objects
            # so that the next access of any attribute, or any query execution
            # will retrieve new state
            session.remove()
        else:
            session.close()

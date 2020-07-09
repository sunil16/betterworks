# -*- coding: utf-8 -*-

import json
import falcon
from app.log import LOG
from app.errors import InvalidParameterError


class JSONTranslator(object):

    def process_request(self, req, res):
        LOG.debug('JSONTranslator start')
        if req.content_type == 'application/json':
            try:
                raw_json = req.stream.read()
            except Exception:
                LOG.debug('stream error')
                message = 'Read Error'
                raise falcon('Bad request', message)

            try:
                req.context['data'] = json.loads(raw_json.decode('utf-8'))
                LOG.debug('JSONTranslator done..')
            except ValueError:
                LOG.debug('JSONTranslator InvalidParameterError: Invalid JSON parmeters')
                raise InvalidParameterError('No JSON object could be decoded or Malformed JSON')
            except UnicodeDecodeError:
                LOG.debug('JSONTranslator UnicodeDecodeError')
                raise InvalidParameterError('Cannot be decoded by utf-8')
        else:
            req.context['data'] = None

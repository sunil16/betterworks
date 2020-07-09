# -*- coding: utf-8 -*-

import sys
import logging

from app import config
from colorlog import ColoredFormatter


class CustomLog:
    def __init__(self, name, level, env: str):
        pass

    def log(*args):
        logging.info(' '.join(map(str, args)))


logging.basicConfig(level=config.LOG_LEVEL)
LOG = logging.getLogger("API")
LOG.propagate = False

INFO_FORMAT = "[%(asctime)s] [%(process)d] [%(levelname)s] %(message)s \n[in %(pathname)s:%(lineno)d]"
DEBUG_FORMAT = "%(reset)s%(log_color)s[%(asctime)s] [%(process)d] [%(levelname)s]\n%(message)s"
# DEBUG_FORMAT = "%(reset)s%(log_color)s[%(asctime)s] [%(process)d] [%(levelname)s] [%(pathname)s:%(lineno)d]\n%(message)s"
# TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S %z"

if config.APP_ENV == "live":
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler("log/app.log", "a", 1 * 1024 * 1024, 10)
    # formatter = logging.Formatter(INFO_FORMAT, TIMESTAMP_FORMAT)
    file_handler.setFormatter(INFO_FORMAT)
    LOG.addHandler(file_handler)


if config.APP_ENV == "dev" or config.APP_ENV == "local":
    stream_handler = logging.StreamHandler(sys.stdout)
    # formatter = logging.Formatter(DEBUG_FORMAT, TIMESTAMP_FORMAT)
    stream_handler.setFormatter(ColoredFormatter(DEBUG_FORMAT, log_colors={
        'DEBUG':    'cyan',
        'INFO':     'green',
        'WARNING':  'yellow',
        'ERROR':    'red',
        'CRITICAL': 'black,bg_red',
    }))
    LOG.addHandler(stream_handler)


def get_logger(name='API'):
    return LOG

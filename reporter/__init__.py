# coding=utf-8

"""
This is the main package for the application.

:copyright: (c) 2013 by Tim Sutton
:license: GPLv3, see LICENSE for more details.
"""

import os
import logging

from flask import Flask


def add_handler_once(logger, handler):
    """A helper to add a handler to a logger, ensuring there are no duplicates.

    Args:
        * logger: logging.logger instance
        * handler: logging.Handler instance to be added. It will not be
            added if an instance of that Handler subclass already exists.

    Returns:
        bool: True if the logging handler was added

    Raises:
        None
    """
    class_name = handler.__class__.__name__
    for myHandler in logger.handlers:
        if myHandler.__class__.__name__ == class_name:
            return False

    logger.addHandler(handler)
    return True


def setup_logger():
    """Set up our logger with sentry support.
    """
    logger = logging.getLogger('osm-reporter')
    logger.setLevel(logging.DEBUG)
    default_handler_level = logging.DEBUG
    # create formatter that will be added to the handlers
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    temp_dir = '/tmp'
    # so e.g. jenkins can override log dir.
    if 'OSM_REPORTER_LOGFILE' in os.environ:
        file_name = os.environ['OSM_REPORTER_LOGFILE']
    else:
        file_name = os.path.join(temp_dir, 'reporter.log')
    file_handler = logging.FileHandler(file_name)
    file_handler.setLevel(default_handler_level)
    # create console handler with a higher log level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    try:
        # pylint: disable=F0401
        # noinspection PyUnresolvedReferences
        from raven.handlers.logging import SentryHandler
        # noinspection PyUnresolvedReferences
        from raven import Client
        # pylint: enable=F0401
        client = Client(
            'http://2e69dbea35044276bc012ea6749104bd:9efad29f86ed4'
            '095bebe745959f7194c@sentry.kartoza.com/25')
        sentry_handler = SentryHandler(client)
        sentry_handler.setFormatter(formatter)
        sentry_handler.setLevel(logging.ERROR)
        add_handler_once(logger, sentry_handler)
        logger.debug('Sentry logging enabled')

    except ImportError:
        logger.debug('Sentry logging disabled. Try pip install raven')

    # Set formatters
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # add the handlers to the logger
    add_handler_once(logger, file_handler)
    add_handler_once(logger, console_handler)

setup_logger()
LOGGER = logging.getLogger('osm-reporter')

app = Flask(__name__)
# Don't import actual view methods themselves - see:
# http://flask.pocoo.org/docs/patterns/packages/#larger-applications
# Also views must be imported AFTER app is created above.
# noinspection PyUnresolvedReferences
from reporter import views

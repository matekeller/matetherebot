import os
import logging
from datetime import datetime, timedelta

try:
    import ujson as json
except ImportError:
    import json

from future.utils import bytes_to_native_str

import tornado.web
from telegram.utils.webhookhandler import WebhookHandler, WebhookServer
from telegram.ext import Updater

max_token = None

LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
logging.basicConfig(level=LOGLEVEL)

class MaxThereState(object):
    def __init__(self):
        self._last_seen = datetime.now() - timedelta(minutes=30)
    def last_seen(self):
        return self._last_seen
    def set_seen(self):
        self._last_seen = datetime.now()

max_there_state = MaxThereState()

class MaxHttpHandler(tornado.web.RequestHandler):
    SUPPORTED_METHODS = ["POST"]

    def __init__(self, application, request, **kwargs):
        super(MaxHttpHandler, self).__init__(application, request, **kwargs)
        self.logger = logging.getLogger(__name__)

    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json; charset="utf-8"')
    
    def post(self):
        self.logger.debug('Max endpoint triggered')
        self._validate_post()
        json_string = bytes_to_native_str(self.request.body)
        data = json.loads(json_string)
        self.logger.debug('Max endpoint received data: ' + json_string)
        if self._validate_payload(data):
            max_there_state.set_seen()
            self.set_status(200)
        else:
            self.set_status(403)


    def _validate_post(self):
        ct_header = self.request.headers.get("Content-Type", None)
        if ct_header != 'application/json':
            raise tornado.web.HTTPError(415)
    
    def _validate_payload(self, data):
        if data.get('max_token', 0) == max_token:
            return True
        else:
            return False
    
    def write_error(self, status_code, **kwargs):
        super(MaxHttpHandler, self).write_error(status_code, **kwargs)
        self.logger.debug("%s - - %s" % (self.request.remote_ip, "Exception in WebhookHandler"),
                          exc_info=kwargs['exc_info'])


class WebhookAppClass(tornado.web.Application):

    def __init__(self, webhook_path, bot, update_queue):
        self.shared_objects = {"bot": bot, "update_queue": update_queue}
        handlers = [
            (r"{0}/?".format(webhook_path), WebhookHandler,
             self.shared_objects),
            (r"/max_present?", MaxHttpHandler)
            ]  # noqa
        tornado.web.Application.__init__(self, handlers)

    def log_request(self, handler):
        pass


def patched_start_webhook(self, listen, port, url_path, cert, key,
                          bootstrap_retries, clean, webhook_url,
                          allowed_updates):
        self.logger.debug('Updater thread started (webhook)')
        if not url_path.startswith('/'):
            url_path = '/{0}'.format(url_path)

        # Create Tornado app instance
        app = WebhookAppClass(url_path, self.bot, self.update_queue)

        # Create and start server
        self.httpd = WebhookServer(listen, port, app, None)

        self.httpd.serve_forever()

def patch_webhook():
    Updater._start_webhook = patched_start_webhook

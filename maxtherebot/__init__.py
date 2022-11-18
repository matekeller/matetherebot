import os

import click
from telegram.ext import Updater

from . import maxthere
from .bot import configure_dispatcher

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

@click.command()
@click.option('--bind', type=str, default='127.0.0.1')
@click.option('--port', type=int, default=8080)
def cli(bind, port):
    maxthere.patch_webhook()
    telegram_token = os.environ['TELEGRAM_TOKEN']
    maxthere_token = os.environ['MAXTHERE_TOKEN']
    webhoook_url = os.environ['WEBHOOK_URL']
    maxthere.max_token = maxthere_token
    updater = Updater(telegram_token, use_context=True)
    configure_dispatcher(updater.dispatcher)
    local_urlpath = telegram_token
    updater.start_webhook(listen=bind, port=port, url_path=local_urlpath)
    updater.bot.set_webhook(webhoook_url)
    updater.idle()
    

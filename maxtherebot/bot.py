from datetime import timedelta, datetime
from telegram.ext import CommandHandler
from telegram import ParseMode

from .maxthere import max_there_state


def maxthere_callback(update, context):
    last_seen = max_there_state.last_seen()
    if datetime.now() - last_seen < timedelta(minutes=5):
        update.message.reply_text('Ich hab Matemenschen in den letzten 5 Minuten noch gesehen')
    elif datetime.now() - last_seen < timedelta(minutes=10):
        update.message.reply_text('Ich hab Matemenschen in den letzten 10 Minuten noch gesehe')
    else:
        update.message.reply_text('Ich glaube Matemenschen ist nicht da.')


def help_callback(update, context):
    update.message.reply_text('Mit dem Befehl /mate kann ich dir sagen wann ich Matemenschen zuletzt im Keller gesehen habe.')


def configure_dispatcher(dispatcher):
    dispatcher.add_handler(CommandHandler('help', help_callback))
    dispatcher.add_handler(CommandHandler('mate', maxthere_callback))

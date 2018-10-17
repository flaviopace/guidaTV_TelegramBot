#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Simple Bot to reply to Telegram messages.

This program is dedicated to the public domain under the CC0 license.

This Bot uses the Updater class to handle the bot.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from parser import htmlparser

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text("Benvenuto " + update.message.from_user.full_name)

def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('/serata -> per sapere i programmi TV di tutte le emittenti televisive per la serata')
    update.message.reply_text('/serata Rai 1-> per sapere i programmi TV della serata per il solo canale Rai 1')
    update.message.reply_text('/serata Rai 2-> per sapere i programmi TV della serata per il solo canale Rai 2')
    update.message.reply_text('/pomeriggio -> per sapere i programmi TV di tutte le emittenti televisive per il pomeriggio')
    update.message.reply_text('/pomeriggio Italia 1 -> per sapere i programmi TV del pomeriggio per il solo canale Italia 1')
    update.message.reply_text('/mattinata -> per sapere i programmi TV di tutte le emittenti televisive per la mattinata')

    update.message.reply_text('...')


def callparser(update, args, url):

    update.message.reply_text("Sto processando le informazioni...")

    hp = htmlparser(url)

    programlist = hp.getPalimpsest()

    channelreq = ' '.join(args).lower()

    if not channelreq:
        for key, values in programlist.iteritems():
            update.message.reply_text("Emittente: {}".format(values[0]))
            for i in range(1, len(values), 2):
                update.message.reply_text("{} : {}".format(values[i].encode('utf-8').strip(),
                                                           values[i + 1].encode('utf-8').strip()))
    else:
        channelnotfound = True
        # user requested a channel
        for key, values in programlist.iteritems():
            if values[0].lower() == channelreq:
                channelnotfound = False
                update.message.reply_text("Emittente scelta: {}".format(values[0]))
                for i in range(1, len(values), 2):
                    update.message.reply_text("{} : {}".format(values[i].encode('utf-8').strip(),
                                                               values[i + 1].encode('utf-8').strip()))

        if channelnotfound:
            update.message.reply_text("Emittente {} non trovata!".format(channelreq))

def echo(bot, update):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def serata(bot, update, args):

    callparser(update, args, "https://hyle.appspot.com/palinsesto/serata")

def pomeriggio(bot, update, args):

    callparser(update, args, "https://hyle.appspot.com/palinsesto/pomeriggio")

def mattina(bot, update, args):

    callparser(update, args, "https://hyle.appspot.com/palinsesto/mattina")

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("632497717:AAHJ1973wsuEW0ZZOvWmlSUkRkZ3OAy3KjY")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("serata", serata, pass_args=True))
    dp.add_handler(CommandHandler("pomeriggio", pomeriggio, pass_args=True))
    dp.add_handler(CommandHandler("mattina", mattina, pass_args=True))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()

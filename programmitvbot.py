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
from parser import superguidatvtvparser


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

urllist = [
    'https://www.superguidatv.it/serata/oggi/premium/',

    'https://www.superguidatv.it/serata/oggi/sky-cinema/',

    'https://www.superguidatv.it/serata/oggi/sky-sport/',

    'https://www.superguidatv.it/serata/oggi/sky-intrattenimento/',
]

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text("Benvenuto " + update.message.from_user.full_name)

def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('/serata -> per sapere i programmi TV di tutte le emittenti televisive (Nazionali, '
                              'Mediaset Premium, Sky Cinema, Sky Sport e Sky Intrattenimento per la serata')
    update.message.reply_text('/serata Rai 1-> per sapere i programmi TV della serata per il solo canale Rai 1')
    update.message.reply_text('/serata Sky Passion-> per sapere i programmi TV della serata per il solo canale Sky '
                              'Passion')
    update.message.reply_text('/serata Premium Action -> per sapere i programmi TV della serata per il solo canale '
                              'Premium Action')
    update.message.reply_text('/serata Premium -> per sapere i programmi di Mediaset Premium')
    update.message.reply_text('/serata Sky-Cinema -> per sapere i programmi di Sky Cinema')
    update.message.reply_text('/serata Sky-Sport -> per sapere i programmi di Sky Sport')
    update.message.reply_text('/serata Sky-Intrattenimaneto -> per sapere i programmi di Sky Intrattenimento')
    update.message.reply_text('/pomeriggio -> per sapere i programmi TV di tutte le emittenti televisive per il '
                              'pomeriggio')
    update.message.reply_text('/pomeriggio Italia 1 -> per sapere i programmi TV del pomeriggio per il solo canale '
                              'Italia 1')
    update.message.reply_text('/mattinata -> per sapere i programmi TV di tutte le emittenti televisive per la'
                              ' mattinata')

    update.message.reply_text('...')


def callparser(update, args, url):

    update.message.reply_text("Sto processando le informazioni...")

    if 'serata' in url:
        hp = superguidatvtvparser(url)
        stepinclist = 3
    else:
        hp = htmlparser(url)
        stepinclist = 2

    programlist = hp.getPalimpsest()

    channelreq = ' '.join(args).lower()

    if not channelreq:
        for key, values in programlist.iteritems():
            update.message.reply_text("Emittente: {}".format(values[0]))
            for i in range(1, len(values), stepinclist):
                if stepinclist != 2:
                    update.message.reply_text("{} : {} - {}".format(values[i].encode('utf-8').strip(),
                                                                    values[i + 1].encode('utf-8').strip(),
                                                                    values[i + 2].encode('utf-8').strip())
                                              )
                else:
                    update.message.reply_text("{} : {}".format(values[i].encode('utf-8').strip(),
                                                           values[i + 1].encode('utf-8').strip()))
    else:
        channelnotfound = True
        # user requested a channel
        for key, values in programlist.iteritems():
            if channelreq in values[0].lower():
                channelnotfound = False
                update.message.reply_text("Emittente scelta: {}".format(values[0]))
                for i in range(1, len(values), stepinclist):
                    if stepinclist != 2:
                        update.message.reply_text("{} : {} - {}".format(values[i].encode('utf-8').strip(),
                                                                        values[i + 1].encode('utf-8').strip(),
                                                                        values[i + 2].encode('utf-8').strip())
                                                  )
                    else:
                        update.message.reply_text("{} : {}".format(values[i].encode('utf-8').strip(),
                                                                   values[i + 1].encode('utf-8').strip()))


        if channelnotfound:
            update.message.reply_text("Emittente {} non trovata!".format(channelreq))

def callfilmparser(update, args, url):

    update.message.reply_text("Sto processando le informazioni...")

    hp = superguidatvtvparser(url)
    stepinclist = 4

    programlist = hp.getPalimpsest()

    channelreq = ' '.join(args).lower()

    if not channelreq:
        for key, values in programlist.iteritems():
            update.message.reply_text("-- Emittente: {}".format(values[0]))
            for i in range(1, len(values)):
                update.message.reply_text("{}".format(values[i].replace("&nbsp;", "")))

    else:
        channelnotfound = True
        # user requested a channel
        for key, values in programlist.iteritems():
            if channelreq in values[0].lower():
                channelnotfound = False
                update.message.reply_text("Emittente scelta: {}".format(values[0]))
                for i in range(1, len(values), stepinclist):
                    update.message.reply_text("{} : {} - {}".format(values[i].encode('utf-8').strip(),
                                                                    values[i + 1].encode('utf-8').strip(),
                                                                    values[i + 2].encode('utf-8').strip(),
                                                                    values[i + 3].encode('utf-8').strip())
                                                  )


        if channelnotfound:
            update.message.reply_text("Emittente {} non trovata!".format(channelreq))


def echo(bot, update):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def serata(bot, update, args):

    if len(args) > 0:
        for singleurl in urllist:
            if args[0].lower() in singleurl:
                args.remove(args[0])
                callparser(update, args, singleurl)
                return


    callparser(update, args, "https://www.superguidatv.it/serata/")

    callparser(update, args, "https://www.superguidatv.it/serata/oggi/premium/")

    callparser(update, args, "https://www.superguidatv.it/serata/oggi/sky-cinema/")

    callparser(update, args, "https://www.superguidatv.it/serata/oggi/sky-sport/")

    callparser(update, args, "https://www.superguidatv.it/serata/oggi/sky-intrattenimento/")


def film(bot, update, args):

    callfilmparser(update, args, "https://www.superguidatv.it/film-in-tv/oggi/nazionali/serata/")

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
    dp.add_handler(CommandHandler("film", film, pass_args=True))


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

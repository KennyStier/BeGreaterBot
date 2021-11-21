#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
Telegram bot to support those who are working to Be Greater.

Created by Kenny
"""

import logging
import random
import datetime
import config

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from dbhelper import DBHelper

db = DBHelper()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

db.setup()

# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi, {user.mention_markdown_v2()}\!',
    )
    db.add_item(update.message.chat_id, "", "")
    update.message.reply_text("Add your streak using the /setstreak command")
    update.message.reply_text("Like so: /setstreak 2020-03-16")



def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help! (I need somebody) Help! (Not just anybody)')

def about(update, context):
    update.message.reply_text('Bot by Stier')

def tempted(update, context):
    easeTemptation = ['God is watching after you', 
                    'We are in this together',
                    'Pray to God, be thankful for all he has given you', 
                    'Go work out', 
                    '\"Virtue is nothing without the trial of temptation, for there is no conflict without an enemy, no victory without strife.\" - Pope St. Leo the Great', 
                    '\"There is no more evident sign that anyone is a saint and of the number of the elect, than to see him leading a good life and at the same time a prey to desolation, suffering, and trials.\" - Saint Aloysius Gonzaga', 
                    '\"If thy right eye scandalize thee, pluck it out and cast it from thee. For it is expedient for thee that one of thy members should perish, rather than that thy whole body be cast into hell.\" - Matthew 5:29'
                    ]
    update.message.reply_text(random.choice(easeTemptation))

def setstreak(update, context):
    db.mod_streak(update.message.chat_id, str(context.args[0]))
    update.message.reply_text("Free from the chains since " + str(context.args[0]))

def deleteData(update, context):
    db.delete_item(update.message.chat_id)
    update.message.reply_text("Your data has been erased.")

def streak(update, context):
    """
    streakYear = db.get_streak(update.message.chat_id)[0:3]
    streakMonth = db.get_streak(update.message.chat_id)[5:6]
    streakDay = db.get_streak(update.message.chat_id)[8:9]
    streakDate = datetime.date(streakYear, streakMonth, streakDay)
    currentYear = (datetime.datetime.now()).strftime("%Y")
    currentMonth = (datetime.datetime.now()).strftime("%m")
    currentDay = (datetime.datetime.now()).strftime("%d")
    currentDate = datetime.date(currentYear, currentMonth, currentDay)
    streakLength = (currentDate-streakDate).days
    """
    update.message.reply_text("Free from the chains since " + db.get_streak(update.message.chat_id)[0]) + "!"

def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(config.botKey)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("about", about))
    dispatcher.add_handler(CommandHandler("setstreak", setstreak))
    dispatcher.add_handler(CommandHandler("streak", streak))
    dispatcher.add_handler(CommandHandler("delete", deleteData))
    dispatcher.add_handler(CommandHandler("tempted", tempted))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
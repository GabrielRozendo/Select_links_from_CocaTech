#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""Simple Bot to send Telegram messages."""

import logging
import os.path

from telegram.ext import CommandHandler, Updater

import ConnectionDB
from AppConfig import GetTelegramToken, GetValue
from Classes import GetTime

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

dispatcher = None
destinatarios = []


def send_message(msg):
    if not destinatarios:
        iniciarbot()
    for destinatario in destinatarios:
        telegramBot.send_message(destinatario['id'], text=msg)

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    chat_id = update.message.chat_id
    update.message.reply_text('Hi! You will receive the links as soon they catched here')
    
    ConnectionDB.InsertTelegramConversation('nome', 'user', chat_id)
    update.message.reply_text('ID: {} saved!'.format(chat_id))


def msghelp(bot, update):
    update.message.reply_text('Dá um start aí e espera')

def stop(bot, update):
    update.message.reply_text('Ok, no more msgs')


def LetsGo(bot, job):
    try:
        logger.info('Let\'s Go rodando...')
        for destinatario in destinatarios:
            bot.send_message(destinatario, text='Link às '+ GetTime())

    except Exception as e:
        logger.warning('LetsGo caused error {}'.format(str(e)))

def alarm(bot, job):
    """Send the alarm message."""
    bot.send_message(job.context, text='Beep!')


def set_timer(bot, update, args, job_queue, chat_data):
    """Add a job to the queue."""
    chat_id = update.message.chat_id
    try:
        # args[0] should contain the time for the timer in seconds
        due = int(args[0])
        if due < 0:
            update.message.reply_text('Sorry we can not go back to future!')
            return

        # Add job to queue
        job = job_queue.run_repeating(alarm, due, context=chat_id)
        job.interval = due
        job.repeat = True
        chat_data['job'] = job

        update.message.reply_text('Timer successfully set!')

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /set <seconds>')




def unset(bot, update, chat_data):
    """Remove the job if the user changed their mind."""
    if 'job' not in chat_data:
        update.message.reply_text('You have no active timer')
        return

    job = chat_data['job']
    job.schedule_removal()
    del chat_data['job']

    update.message.reply_text('Timer successfully unset!')


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def iniciarbot():
    token = GetTelegramToken()
    logger.info('Carregando Bot...')

    global telegramBot
    telegramBot = Updater(token).dispatcher.bot
    
    global destinatarios
    destinatarios = ConnectionDB.ReadAllTelegramConversation()
    logger.info('{} destinatarios'.format(len(destinatarios)))

def main():
    """Run bot."""

    token = GetTelegramToken()
    logger.info('Bot Iniciando...')

    updater = Updater(token)
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
                                
    dp.add_handler(CommandHandler("help", msghelp))
    #dp.add_handler(CommandHandler("set", set_timer,
    #                              pass_args=True,
    #                              pass_job_queue=True,
    #                              pass_chat_data=True))
    dp.add_handler(CommandHandler("unset", unset, pass_chat_data=True))

    # log all errors
    dp.add_error_handler(error)
 

    # Start the Bot
    updater.start_polling()
    updater.bot.send_message(65045026, text='Bot iniciado :)\t {}!'.format(GetTime()))
    
    due = 30
    job = updater.job_queue.run_repeating(LetsGo, due)
    job.interval = due
    job.repeat = True
    updater.chat_data['job'] = job


    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()

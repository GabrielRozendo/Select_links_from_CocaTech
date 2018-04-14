#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""Simple Bot to send Telegram messages."""

import logging
import os.path

import telegram
from telegram.ext import CommandHandler, Updater

import Classes
import ConnectionDB
from AppConfig import GetTelegramToken, GetValue
from Classes import GetTime

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
                    level=logging.INFO)

logger = logging.getLogger(__name__)

cacheUsers = ConnectionDB.ReadAllTelegramUsers()


def start(bot, update, chat_data):
    chat_id = update.message.chat_id
    username = update.message.from_user.name
    name = update.message.from_user.full_name
    ativo = ConnectionDB.UsuarioAtivo(chat_id)
    if ativo:
         update.message.reply_text('Hi {}! You already started the bot. Be patience and wait for the links...'.format(name))
    else:
        update.message.reply_text('Hi {}! You will receive the links as soon we catched them here'.format(name))
        ConnectionDB.InsertTelegramConversation(chat_id, name, username)
        cacheUsers.append(chat_id)
        update.message.reply_text('Thanks {} ({}). You are saved!'.format(name, username))


def unset(bot, update, chat_data):
    chat_id = update.message.chat_id
    username = update.message.from_user.name
    name = update.message.from_user.full_name
    ativo = Classes.InList(cacheUsers, chat_id)
    if ativo:
        ConnectionDB.InativarTelegramConversation(chat_id)
        cacheUsers.remove(chat_id)
        update.message.reply_text('Hi {}! You exited and will not receive more links...'.format(name))
    else:
        update.message.reply_text('Hi {}! You already exited and are not in list to receive new posts.'.format(name))
    
    update.message.reply_text('Whenever you want, send /start to come back...')


def msghelp(bot, update):
    update.message.reply_text('Dá um start aí e espera')


def LetsGo(bot, job):
    try:
        logger.info('Let\'s Go rodando para {} users...'.format(len(cacheUsers)))
        for user in cacheUsers:
            bot.send_message(user['id'], 
                            text='*Link* _às_ [link]({}) `{}`'.format('http://google.com', GetTime()),
                            parse_mode=telegram.ParseMode.MARKDOWN)

    except Exception as e:
        logger.warning('LetsGo caused error {}'.format(str(e)))


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def send_message(msg):
    try:
        logger.info('Send message rodando para {} users...'.format(len(cacheUsers)))
        logger.info('Msg para enviar: {}'.format(msg))
        for user in cacheUsers:
            dp.bot.send_message(user['id'], text=msg, parse_mode=telegram.ParseMode.MARKDOWN)

    except Exception as e:
        logger.warning('LetsGo caused error {}'.format(str(e)))

token = GetTelegramToken()
logger.info('Bot Iniciando...')

updater = Updater(token)

# Get the dispatcher to register handlers
dp = updater.dispatcher

# on different commands - answer in Telegram
dp.add_handler(CommandHandler("start", start, pass_chat_data=True))
                            
dp.add_handler(CommandHandler("help", msghelp))
#dp.add_handler(CommandHandler("set", set_timer,
#                              pass_args=True,
#                              pass_job_queue=True,
#                              pass_chat_data=True))
dp.add_handler(CommandHandler("unset", unset, pass_chat_data=True))
#dp.add_handler(CommandHandler("stop", stop, pass_chat_data=True))

# log all errors
dp.add_error_handler(error)

# Start the Bot
updater.start_polling()

dp.bot.send_message(65045026, text='Bot iniciado com {} usuarios e {} em cache\t😁\t {}!'.format(ConnectionDB.QtTelegramUsers(), len(cacheUsers), GetTime()))

# due = 30
# job = dp.job_queue.run_repeating(LetsGo, due)
# job.interval = due
# job.repeat = True
# dp.chat_data['job'] = job


# Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
# SIGABRT. This should be used most of the time, since start_polling() is
# non-blocking and will stop the bot gracefully.
updater.idle()

#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""Simple Bot to send Telegram messages."""

import logging
import os.path

import telegram
from telegram.ext import CommandHandler, Updater

import ConnectionDB
from AppConfig import GetTelegramToken, GetValue
import Classes

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

cachedUsers = ConnectionDB.ReadAllTelegramUsers()
dispatcher = None


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
        cachedUsers.append(chat_id)
        update.message.reply_text('Thanks {} ({}). You are saved!'.format(name, username))


def unset(bot, update, chat_data):
    chat_id = update.message.chat_id
    # username = update.message.from_user.name
    name = update.message.from_user.full_name
    ativo = Classes.InList(cachedUsers, chat_id)
    if ativo:
        ConnectionDB.InativarTelegramConversation(chat_id)
        cachedUsers.remove(chat_id)
        update.message.reply_text('Hi {}! You exited and will not receive more links...'.format(name))
    else:
        update.message.reply_text('Hi {}! You already exited and are not in list to receive new posts.'.format(name))
    
    update.message.reply_text('Whenever you want, send /start to come back...')


def send_message(msg):
    try:
        if dispatcher is None:
            iniciarbot()
        logger.info('Send message rodando para {} users...'.format(len(cachedUsers)))
        logger.info('Msg para enviar: {}'.format(msg))
        for user in cachedUsers:
            dispatcher.bot.send_message(user['id'], text=msg, parse_mode=telegram.ParseMode.MARKDOWN)

    except Exception as e:
        logger.warning('LetsGo caused error {}'.format(str(e)))


def msghelp(bot, update):
    update.message.reply_text('Dá um start aí e espera')


def LetsGo(bot, job):
    try:
        logger.info('Let\'s Go rodando para {} users...'.format(len(cachedUsers)))
        for user in cachedUsers:
            bot.send_message(user['id'], 
                            text='*Link* _às_ [link]({}) `{}`'.format('http://google.com', Classes.GetTime()),
                            parse_mode=telegram.ParseMode.MARKDOWN)

    except Exception as e:
        logger.warning('LetsGo caused error {}'.format(str(e)))


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)



def iniciarbot():
    token = GetTelegramToken()
    logger.info('Carregando Bot...')

    global dispatcher
    dispatcher = Updater(token).dispatcher

    global cachedUsers
    if cachedUsers is None:    
        cachedUsers = ConnectionDB.ReadAllTelegramUsers()
    logger.info('{} destinatários'.format(len(cachedUsers)))


def main():
    """Run bot."""

    token = GetTelegramToken()
    logger.info('Bot Iniciando...')

    updater = Updater(token)
    global dispatcher
    dispatcher = updater.dispatcher


    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start, pass_chat_data=True))
                                
    dispatcher.add_handler(CommandHandler("help", msghelp))
    #dp.add_handler(CommandHandler("set", set_timer,
    #                              pass_args=True,
    #                              pass_job_queue=True,
    #                              pass_chat_data=True))
    dispatcher.add_handler(CommandHandler("unset", unset, pass_chat_data=True))
    #dp.add_handler(CommandHandler("stop", stop, pass_chat_data=True))
        # log all errors
    dispatcher.add_error_handler(error)
 

    # Start the Bot
    updater.start_polling()
    
    due = 30
    job = updater.job_queue.run_repeating(LetsGo, due)
    job.interval = due
    job.repeat = True
    dispatcher.chat_data['job'] = job

    dispatcher.bot.send_message(65045026, text='Bot iniciado com {} usuarios e {} em cache\t😁\t {}!'.format(ConnectionDB.QtTelegramUsers(), len(cachedUsers), Classes.GetTime()))

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()

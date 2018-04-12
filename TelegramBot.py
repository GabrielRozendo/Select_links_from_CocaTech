from AppConfig import GetTelegramToken
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler
import logging


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# https://github.com/python-telegram-bot/python-telegram-bot/wiki/Introduction-to-the-API
# https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/timerbot.py

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")


def sayhi(updater, bot, job):
    job.context.message.reply_text('Hello {}'.format(updater.message.from_user.first_name))

def time(updater, bot, update,job_queue):
    job = job_queue.run_repeating(sayhi, 5, context=update)

def main():
    token = GetTelegramToken()
    updater = Updater(token)
    dp = updater.dispatcher

    
    dp.add_handler(MessageHandler(Filters.text , time, pass_job_queue=True))


    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()


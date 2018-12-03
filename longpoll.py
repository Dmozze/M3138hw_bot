#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import logging

from config import *

logging.basicConfig(format='%(asctime)s - %(name)s - '
                           '%(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename=HOME + 'bot.log')
logger = logging.getLogger(__name__)

students = {}

def start(bot, update):
    update.message.reply_text(
        'Привет! Я бот, который поможет тебе, как можно быстрее выйти к доске (или нет)\n'
        'Перед использованием советую ознакомится с основами /help'
    )

    


def help(bot, update):
    update.message.reply_text(
        'Чтобы начать пользоваться ботом нужно зарегистрироваться /reg\n'
        '/reg принимает вашу фамилию с большой буквы\n'
        'После регистрации нужно внести свою задачу в бот /edit\n'
        '/edit принимает ваши задачи через пробел, если задачи не было он ее добавит, иначе исключит из списка задач на следующую практик\n'
        '/show показывает, какие задачи заявлены на следующую практику\n'
        'При возникновении проблем писать @Dmozze'
    )

def checkIn(bot, update, args){
    if (len(args) != 1){
        update.message.reply_text('Неверное количество аргументов, введите только фамилию с заглавной буквы')
        return;
    }
    for i in lastnames
        if (args == i[0:len(args)):
            
            break;
    
def error(bot, update, info):
    logger.warning('Update "%s" caused error "%s"', update, info)

if __name__ == '__main__':
    
    updater = Updater(TOKEN)    
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CommandHandler('reg', checkIn))
    dp.add_handler(CommandHandler('edit', edit))
    dp.add_handler(CommandHandler('show', show))

    dp.add_handler(CommandHandler('l', list))
    dp.add_handler(CommandHandler('r', random))
    dp.add_handler(CommandHandler('n', choose));


    dp.add_error_handler(error)
    
    updater.start_polling()
    updater.idle()

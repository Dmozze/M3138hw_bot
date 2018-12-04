#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler

import logging
import shelve

from config import *

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

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


def checkIn(bot, update, args):
    name = str(args[0])
    if (len(args) != 1):
        update.message.reply_text('Неверное количество аргументов, введите только фамилию с заглавной буквы')
        return
    isnamegood = False
    print(len(lastnames))
    for i in range(len(lastnames)):
        print (lastnames[i][0:len(name)])
        if (name == lastnames[i][0:len(name)]):
            db = shelve.open('names')
            db[str(update.message.chat_id)] = i
            lastnames[i] = ''
            isnamegood = True
            break
    if isnamegood:
        update.message.reply_text('Вы были удачно зарегистрированны')
    else:
        update.message.reply_text('Я не смог вас индефицировать, как студента M3138')

def edit(bot, update, args):
    id = str(update.message.chat_id)
    with shelve.open('names', flag='r') as shelve_names:
        if id in shelve_names:
            with shelve.open('tasks') as shelve_tasks:
                shelve_tasks[id] = args
        else:
            update.message.reply_text('Вы не зарегистрированы, /help')
    return

def show(bot,update):
    id = str(update.message.chat_id)
    with shelve.open('names', flag='r') as shelve_names:
        if id in shelve_names:
            with shelve.open('tasks') as shelve_tasks:
                if id in shelve_tasks:
                    answer = ' '.join(shelve_tasks[id])
                    print(answer)
                    if len(answer) == 0:
                        update.message.reply_text('Вы заявили 0 задач(')
                    else:
                        update.message.reply_text(answer)
                else:
                    update.message.reply_text('Вы заявили 0 задач(')
        else:
            update.message.reply_text('Вы не зарегистрированы, /help')
    return


def error(bot, update, info):
    logger.warning('Update "%s" caused error "%s"', update, info)


if __name__ == '__main__':
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CommandHandler('reg', checkIn, pass_args=True))
    dp.add_handler(CommandHandler('edit', edit, pass_args=True))
    dp.add_handler(CommandHandler('show', show))

#    dp.add_handler(CommandHandler('l', list))
#    dp.add_handler(CommandHandler('r', random))
#    dp.add_handler(CommandHandler('n', choose));

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

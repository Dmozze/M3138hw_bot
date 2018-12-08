#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler

import logging
import shelve

from config import *
from externalfunctions import *
from upload import *

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )

logger = logging.getLogger(__name__)

def checkUserName(username):
    if username != None and (username.lower() == TEACHER_USERNAME or username.lower() == ADMIN_USERNAME):
        return True
    else:
        return False

def debug(bot, update):
    if not checkUserName(update.message.from_user.username):
        update.message.reply_text('У вас недостаточно прав для выполнения указанной команды')
        return

def start(bot, update):
    if checkUserName(update.message.from_user.username):
        update.message.reply_text(
            'Здравствуйте, я бот, который умеет собирать листочки\n'
            'Перед использованием советую ознакомиться с основами /help'
        )
    else:
        update.message.reply_text(
            'Привет! Я бот, который умеет принимать листочки без листочков\n'
            'Перед использованием советую ознакомится с основами /help'
        )


def help(bot, update):
    if checkUserName(update.message.from_user.username):
        update.message.reply_text(
        '/update - Обновить сданные задачи (aka Собрать листочки)\n'
        )
    else:
        update.message.reply_text(
            '/reg `Фамилия` - зарегистрироваться под `Фамилией`\n'
            '/add `Номера задач через пробел` - добавить задачи\n'
            '/remove `Номера задач через пробел` - удалить задачи\n'
            '/add и /remove поддерживают ввод отрезками\n'
            'Пример: /add 125 126-129 126-130 - вам будут добавлены задачи [125 .. 130]\n'
            '/clear - очистит список ваших задач\n'
            '/show - показывает список ваших задач\n'
            'Отзывы и предложения сюда: `@Dmozze`',
            parse_mode='Markdown'
        )


def checkIn(bot, update, args):
    if (len(args) != 1):
        update.message.reply_text('Неверное количество аргументов, введите только фамилию')
        return
    name = str(args[0])
    for i in lastnames:
        if (name.lower() == i[0:len(name)].lower()):
            with shelve.open('names_db') as shelve_names:
                user_id = str(update.message.chat_id)
                if user_id in shelve_names:
                    update.message.reply_text('Вы уже зарегистрированы как ' + shelve_names[user_id]['name'])
                    return
                shelve_names[user_id] = {'name' : i, 'tasks' : []}
                update.message.reply_text('Вы были удачно зарегистрированны')
                return
    update.message.reply_text('Я не смог вас идентифицировать как студента M3138')

def is_correct_value(value):
    if value.isdigit() and int(value) > 0 and int(value) < 200:
        return True
    else:
        return False

def clear(bot, update):
    with shelve.open('names_db',writeback=True) as shelve_names:
        user_id = str(update.message.chat_id)
        if user_id not in shelve_names:
            update.message.reply_text('Вы не зарегистрированы, смотрите /help')
            return
        shelve_names[user_id]['tasks'] = []
    show(bot,update)

def good_set(array):
    invalues = set()
    for value in array:
        if is_correct_value(value):
            invalues.add(int(value))
        else:
            rng = value.split('-')
            if len(rng) == 2 and is_correct_value(rng[0]) and is_correct_value(rng[1]):
                for number in range(int(rng[0]), int(rng[1]) + 1):
                    invalues.add(number)
    return invalues

def add(bot, update,args):
    with shelve.open('names_db',writeback=True) as shelve_names:
        user_id = str(update.message.chat_id)
        if user_id not in shelve_names:
            update.message.reply_text('Вы не зарегистрированы, смотрите /help')
            return
        toadd = good_set(args)
        shelve_names[user_id]['tasks'] = sorted(list(set(shelve_names[user_id]['tasks']) | toadd))
    show(bot,update)

def remove(bot, update,args):
    with shelve.open('names_db',writeback=True) as shelve_names:
        user_id = str(update.message.chat_id)
        if user_id not in shelve_names:
            update.message.reply_text('Вы не зарегистрированы, смотрите /help')
            return
        toremove = good_set(args)
        shelve_names[user_id]['tasks'] = sorted(list(set(shelve_names[user_id]['tasks']) - toremove))
    show(bot,update)

def show(bot,update):
    with shelve.open('names_db') as shelve_names:
        user_id = str(update.message.chat_id)
        if user_id not in shelve_names:
            update.message.reply_text('Вы не зарегистрированы, смотрите /help')
            return
        if len(shelve_names[user_id]['tasks']) == 0:
            update.message.reply_text('Список ваших задач пуст')
        else:
            update.message.reply_text('Вы заявили задачи под номерами: ' + ', '.join([str(i) for i in shelve_names[user_id]['tasks']]))

def update(bot,update):
    if not checkUserName(update.message.from_user.username):
        update.message.reply_text('У вас недостаточно прав для выполнения указанной команды')
        return
    unsolvedtasks = upload()
    data = []
    with shelve.open('names_db') as shelve_names:
        for tasknumber in unsolvedtasks:
            solvedby = [str(tasknumber)]
            for id in shelve_names.keys():
                if tasknumber in shelve_names[id]['tasks']:
                    solvedby.append(shelve_names[id]['name'])
            if len(solvedby) > 1:
                data.append(sorted(solvedby))
    print(data)
    generate_csv_file(data)
    update.message.reply_document(open('sheet.csv', 'rb'))

def error(bot, update, info):
    logger.warning('Update "%s" caused error "%s"', update, info)


if __name__ == '__main__':
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    #public handlers
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CommandHandler('reg', checkIn, pass_args=True))
    dp.add_handler(CommandHandler('show', show))
    #dp.add_handler(CommandHandler('csv', csv))
    dp.add_handler(CommandHandler('clear', clear))
    dp.add_handler(CommandHandler('remove', remove, pass_args=True))
    dp.add_handler(CommandHandler('add', add, pass_args=True))
    #privatehandlers
    dp.add_handler(CommandHandler('update', update))
    dp.add_handler(CommandHandler('debug', debug))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

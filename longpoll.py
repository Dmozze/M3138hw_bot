#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler

import logging
import shelve

from config import *
from externalfunctions import *

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    #filename=HOME + 'bot.log'
                    )

logger = logging.getLogger(__name__)

def checkUserName(username):
    if username.lower() == TEACHER_USERNAME or username.lower() == ADMIN_USERNAME:
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
            '/reg `Фамилия` зарегистрироваться под `Фамилией`\n'
            '/edit принимает ваши задачи через пробел, если задачи не было, он ее добавит, иначе исключит из списка задач на следующую практику\n'
            '/show показывает, какие задачи заявлены на следующую практику\n'
            '/csv - In development'
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
                    update.message.reply_text('Вы уже зарегистрированы как ' + i)
                    return
                shelve_names[user_id] = {'name' : lastname[i].split()[0], 'tasks' : []}
                update.message.reply_text('Вы были удачно зарегистрированны')
                return
    update.message.reply_text('Я не смог вас идентифицировать как студента M3138')

def is_correct_value(value):
    if value.isdigit() and int(value) > 0 and int(value) < 200:
        return True
    else:
        return False

def edit(bot, update, args):
    with shelve.open('names_db') as shelve_names:
        user_id = str(update.message.chat_id)
        if user_id not in shelve_names:
            update.message.reply_text('Вы не зарегистрированы, смотрите /help')
            return
        invalues = {}
        for value in args:
            if is_correct_value(value)
                invalues.insert(value)
            else:
                 range = value.split('-')
                 if len(range) == 2 and is_correct_value(range[0]) and is_correct_value(range[1]):
                     for number in range(range[0], range[1] + 1):
                         invalues.insert(number)
        shelve_names[user_id]['tasks'] = list(set(shelve_names) ^ invalues)
        show(bot, update)

def show(bot,update):
    with shelve.open('names_db') as shelve_names:
        user_id = str(update.message.chat_id)
        if user_id not in shelve_names:
            update.message.reply_text('Вы не зарегистрированы, смотрите /help')
            return
        update.message.reply_text('Вы заявили задачи под номерами: ' + ', '.join(shelve_names[user_id][tasks]))

def update(bot,update):
    if not checkUserName(update.message.from_user.username):
        update.message.reply_text('У вас недостаточно прав для выполнения указанной команды')
        return
    unsolvedtasks = update_tasks()
    data = []
    with shelve.open('names_db') as shelve_names:
        for tasknumber in unsolvedtasks:
            solvedby = [tasknumber]
            for person in shelve_names.keys():
                if tasknumber in person['tasks']:
                    solvedby.append(person['name'])
            if len(solvedby) > 1:
                data.append(solvedby)
    generate_csv_file(data)
    update.message.reply_document('sheet.csv')

def error(bot, update, info):
    logger.warning('Update "%s" caused error "%s"', update, info)


if __name__ == '__main__':
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    #public handlers
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CommandHandler('reg', checkIn, pass_args=True))
    dp.add_handler(CommandHandler('edit', edit, pass_args=True))
    dp.add_handler(CommandHandler('show', show))
    dp.add_handler(CommandHandler('csv', csv))

    #privatehandlers
    dp.add_handler(CommandHandler('update', update))
    dp.add_handler(CommandHandler('debug', debug))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

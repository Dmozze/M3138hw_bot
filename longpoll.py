#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler

import logging
import shelve

from config import *
from build import *
from pull import *
import random

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
        '/choose `number` - Вывести людей, которые заявились на задачу  `number`\n'
        '/all - выведет /choose для всех доступных задач\n',
        #'/lose `number` - Использовать, если человек проиграл на задаче `number`. Распределение перестроится автоматически',
        parse_mode='Markdown'
        )
    else:
        update.message.reply_text(
            '/reg `lastname` зарегистрироваться под фамилией `lastname`(lastname --- Ваша фамилия НА РУССКОМ)\n'
            'Обратите внимание, что регистрация обязательна для пользования ботом\n'
            '/edit принимает ваши задачи через пробел, если задачи не было, он ее добавит, иначе исключит из списка задач на следующую практику\n'
            '/show показывает, какие задачи заявлены на следующую практику\n'
            'При возникновении проблем писать `@Dmozze`',
            parse_mode='Markdown'
        )


def checkIn(bot, update, args):
    if (len(args) != 1):
        update.message.reply_text('Неверное количество аргументов, введите только фамилию с заглавной буквы')
        return
    name = str(args[0])
    isnamegood = False
    for i in range(len(lastnames)):
        if (name.lower() == lastnames[i][0:len(name)].lower()):
            db = shelve.open('names')
            if str(update.message.chat_id) in db:
                update.message.reply_text('Вы уже зарегистрированы как ' + lastnames[i])
                return
            db[str(update.message.chat_id)] = i
            lastnames[i] = ''
            isnamegood = True
            break
    if isnamegood:
        update.message.reply_text('Вы были удачно зарегистрированны')
    else:
        update.message.reply_text('Я не смог вас идентифицировать как студента M3138')

def show(bot,update):
    id = str(update.message.chat_id)
    with shelve.open('names', flag='r') as shelve_names:
        if id in shelve_names:
            with shelve.open('tasks') as shelve_tasks:
                if id in shelve_tasks:
                    temp = [str(i) for i in shelve_tasks[id]]
                    temp.sort()
                    answer = ' '.join(str(i) for i in temp)
                    if len(answer) == 0:
                        update.message.reply_text('Вы заявили 0 задач(')
                    else:
                        update.message.reply_text(answer)
                else:
                    update.message.reply_text('Вы заявили 0 задач(')
        else:
            update.message.reply_text('Вы не зарегистрированы, /help')
    return

def edit(bot, update, args):
    in_values = []
    for i in args:
        if i.isdigit() and int(i) > 0 and int(i) < 200:
            in_values.append(int(i))
    id = str(update.message.chat_id)
    with shelve.open('names', flag='r') as shelve_names:
        if id in shelve_names:
            with shelve.open('tasks') as shelve_tasks:
                if id in shelve_tasks:
                    temp = shelve_tasks[id]
                    for j in shelve_tasks[id]:
                        if j in in_values:
                            in_values.remove(j)
                            temp.remove(j)
                    shelve_tasks[id] = list(set(temp + in_values))
                else:
                    shelve_tasks[id] = list(set(in_values))
            show(bot, update)
        else:
            update.message.reply_text('Вы не зарегистрированы, /help')
    return

def update(bot,update):
    if not checkUserName(update.message.from_user.username):
        update.message.reply_text('У вас недостаточно прав для выполнения указанной команды')
        return
    people = []
    with shelve.open('names') as shelve_names:
        for i in shelve_names.keys():
            id = shelve_names[i]
            people.append({'chat_id': str(i),'name': str(lastnames[id].split()[0])})
    alltasks = []
    with shelve.open('tasks') as shelve_tasks:
        for i in people:
            if i['chat_id'] in shelve_tasks:
                i.update({'tasks' : shelve_tasks[i['chat_id']]})
                for j in i['tasks']:
                    alltasks.append(j)
            else:
                i.update({'tasks':[]})
    temp = update_tasks()
    available_tasks = list(temp & set(alltasks))
    available_tasks.sort()
    with shelve.open('dealing') as shelve_deal:
        shelve_deal.clear()
        for i in available_tasks:
            temp = []
            for j in people:
                if i in j['tasks']:
                    temp.append(j['name'])
            if len(temp) != 0:
                 shelve_deal[str(i)] = temp

def all(bot, update):
    if not checkUserName(update.message.from_user.username):
        update.message.reply_text('У вас недостаточно прав для выполнения указанной команды')
        return
    with shelve.open('dealing') as shelve_deal:
        res = ""
        temp =[]
        for i in  shelve_deal.keys():
            temp.append(i)
        temp.sort()
        for i in temp:
            res += str(i) + ' - ' + ', '.join(str(i) for i in shelve_deal[i]) + '\n'
        update.message.reply_text(res)


def choose(bot, update, args):
    if not checkUserName(update.message.from_user.username):
        update.message.reply_text('У вас недостаточно прав для выполнения указанной команды')
        return
    Task_name = str(args[0])
    with shelve.open('dealing') as shelve_deal:
        if Task_name not in shelve_deal:
            update.message.reply_text('Данная задача не была заявлена')
        else:
            update.message.reply_text(Task_name + ' - ' + ', '.join(str(i) for i in shelve_deal[Task_name]))
    return

def lose(bot, update, args):
    if not checkUserName(update.message.from_user.username):
        update.message.reply_text('У вас недостаточно прав для выполнения указанной команды')
        return
    loser_id = str(args[0])
    with shelve.open('dealing') as shelve_deal:
        loser = shelve_deal[loser_id]['id']
        with shelve.open('losers') as shelve_losers:
            shelve_losers[str(loser)] = True
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

    dp.add_handler(CommandHandler('update', update))
    dp.add_handler(CommandHandler('all', all))
    dp.add_handler(CommandHandler('choose', choose, pass_args=True))
    dp.add_handler(CommandHandler('lose', lose, pass_args=True))

    dp.add_handler(CommandHandler('debug',debug))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

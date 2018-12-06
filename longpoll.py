#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler

import logging
import shelve

from config import *
from build import *
from pull import *

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def checkUserName(username):
    if username.lower() == TEACHER_USERNAME or username.lower() == ADMIN_ID:
        return True
    else:
        return False
def start(bot, update):
    if checkUserName(update.message.from_user.username):
        update.message.reply_text(
            'Здравствуйте, я бот, который поможет вам вызвать к доске нуждающихся (или нет)\n'
            'Перед использованием советую ознакомиться с основами /help'
        )
    else:
        update.message.reply_text(
            'Привет! Я бот, который поможет тебе, как можно быстрее выйти к доске (или нет)\n'
            'Перед использованием советую ознакомится с основами /help'
        )


def help(bot, update):
    if checkUserName(update.message.from_user.username):
        update.message.reply_text(
        '/build - сгенерирует новое распределени\n'
        '/all выведет полное распределение\n'
        '/choose `number` - Вызвать человека на задачу `number`\n'
        '/lose `number` - Использовать, если человек проиграл на задаче `number`. Распределение перестроится автоматически',
        parse_mode='Markdown'
        )
    else:
        update.message.reply_text(
            '/reg `Lastname` зарегистрироваться под фамилией `Lastname`(Lastname --- Ваша фамилия с заглавной буквы)\n'
            'Обратите внимание, что регистрация обязательна для пользования ботом\n'
            '/edit принимает ваши задачи через пробел, если задачи не было, он ее добавит, иначе исключит из списка задач на следующую практику\n'
            '/show показывает, какие задачи заявлены на следующую практику\n'
            'При возникновении проблем писать `@Dmozze`',
            parse_mode='Markdown'
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
                    print(temp, in_values)
                    shelve_tasks[id] = list(set(temp + in_values))
                else:
                    shelve_tasks[id] = list(set(in_values))
        else:
            update.message.reply_text('Вы не зарегистрированы, /help')
    return

def show(bot,update):
    id = str(update.message.chat_id)
    with shelve.open('names', flag='r') as shelve_names:
        if id in shelve_names:
            with shelve.open('tasks') as shelve_tasks:
                if id in shelve_tasks:
                    answer = ' '.join([str(i) for i in shelve_tasks[id]])
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

def build(bot,update):
    if not checkUserName(update.message.from_user.username):
        update.message.reply_text('У вас недостаточно прав для выполнения указанной команды')
        return
    people = []
    with shelve.open('names') as shelve_names:
        for i in shelve_names.get_keys():
            id = shelve_names[i]
            people.append({'chat_id': i, 'id':id, 'name': lastnames[id].split()[0] + ' ' + lastnames[id].split()[1][1] + '. ' + lastnames[id].split()[2][1] + '.'})
    with shelve.open('losers') as shelve_losers:
        for i in people:
            if str(i.id) in losers:
                i.update({'lose' : True})
    alltasks = []
    with open shelve.open('tasks') as shelve_tasks:
        for i in people
            i.update({'tasks' : shelve_tasks[i.chat_id]})
            alltasks.append(i.tasks)
    available_tasks = list(update_tasks().intersection_update(set(alltasks)))
    std_score = update_score()
    std_last_task = update_last_task()
    weight = [[0] * available_tasks for i in range(len(people))]

    ## TODO: Сделать нормальные веса.
    dealing = assignment_hungary(weight)
    with shelve.open('dealing') as shelve_deal:
        shelve_deal.clear()
        for i in range(len(dealing)):
            if dealing[i] > 0:
                shelve_deal[str(available_tasks[i - 1])] = people[dealing[i]]

def all(bot, update, args):
    if not checkUserName(update.message.from_user.username):
        update.message.reply_text('У вас недостаточно прав для выполнения указанной команды')
        return
    with shelve.open('dealing') as shelve_deal:
        str = ""
        for i in shelve_deal.get_keys():
            str += str(i) + ' - ' + shelve_deal[i].name + '\n'
     update.message.reply_text(str)


def choose(bot, update, args):
    if not checkUserName(update.message.from_user.username):
        update.message.reply_text('У вас недостаточно прав для выполнения указанной команды')
        return
    Task_name = str(args)
    with shelve.open('dealing') as shelve_deal:
        update.message.reply_text(Task_name + ' - ' + shelve_deal[Task_name].name)
    return

def lose(bot, update, args):
    if not checkUserName(update.message.from_user.username):
        update.message.reply_text('У вас недостаточно прав для выполнения указанной команды')
        return
    loser_id = int(args[0])
    with shelve.open('dealing') as shelve_deal:
        loser = shelve_deal[loser_id].id
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

    dp.add_handler(CommandHandler('build', build))
    dp.add_handler(CommandHandler('all', all))
    dp.add_handler(CommandHandler('choose', choose, pass_args=True))
    dp.add_handler(CommandHandler('lose', lose, pass_args=True))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

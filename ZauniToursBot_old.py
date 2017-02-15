#!/usr/bin/env python
# -*- coding: utf-8 -*-

import telepot
from pymongo import MongoClient
import time
import json
import hashlib
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


TOKEN = "337788209:AAFUYfBAGqvKtkHxKB7stAngOYWJrEq6MpQ"
zt_chat = '-212813651'
maxi_id = '12349793'

MSG_IN_DEV = "Sorry, this function is actually under development!"
MSG_UNKNOWN_USER = "Sorry, Unknown Username!"
MSG_ALLREADY_USER = "You are allready registred!"
MSG_SHOW_USER = "%s: %s &#128; \n"
MSG_SHOW_MONEY = "\t\t\t\t\t\t%s : %s&#128;\n"
MSG_COMMANDS = [
    ["/add transaction_text;value;user1(;user2;user3)", ""],
    ["/show user1;(user2;user3)", ""],
    ["/showhistory user1(;user2;user3)", ""],
    ["/showall", "zeigt alle Nutzer deren Value != 0 ist"],
    ["/showall0", "zeit alle Nutzer"],
    ["/help", ""],
    ["/adduser username1(;user2;user3)", "<dep>"],
    ["/register username", "<dep>"]
]
MSG_STILL_WAITING_REGISTR = "You have still an outstanding registration request"
MSG_NEW_PERMISSION = "Your permissions have been set to %s"
MSG_DEPRECATED = "DEPRECATED"

bot = telepot.Bot(TOKEN)
MONGO = MongoClient("127.0.0.1",27017)["zaunitours"]


def user_get(user_id):
    result = MONGO.zt_users.find_one({"user_id": user_id})
    return result


def user_register(id, permission):
    data = MONGO.zt_users.find_one({"id": id})
    result = MONGO.zt_users.update_one({"id": id}, {"$set": {"permission": permission},
                                                    "$rename": {"_name": "name", "_user_id": "user_id"},
                                                    "$unset": {"msg_id_0": "", "msg_id_1": ""}
                                                    }, upsert=False)
    tup = (data['msg_id_0'], data['msg_id_1'])
    telepot.helper.Editor(bot, tup).editMessageReplyMarkup(reply_markup=None)
    telepot.helper.Editor(bot, tup).editMessageText("%s have set to %s" % (data['_name'], permission))
    if result.raw_result["ok"] is not 1 or result.acknowledged is False:
        raise Exception("mongo update")
    return 0


def get_user(nick):
    result = MONGO.zt_users.find_one({"nick": nick})
    return result


def user_add(nick, user_id):
    if get_user(nick) is not None:
        return 1
    money = {
        "time": str(time.strftime("%Y-%m-%d---%H:%M:%S")),
        "text": "&lt;start&gt;",
        "value": 0,
        "by": user_id
    }
    id = hashlib.sha256(json.dumps(money)).hexdigest()[:16]
    result = MONGO.zt_users.update_one({"id": id}, {"$set": {"permission": 0, "nick": nick, "value": 0, "money": [money]}}, upsert=True)
    if result.raw_result["ok"] is not 1 or result.acknowledged is False:
        raise Exception("mongo update")
    return 0


def add(chat_id, user_id, value):
    tmp = value.split(";")
    if tmp.__len__() < 3:
        bot.sendMessage(chat_id, "usage: /add text;value;user(;user2;user3)")
        return 0
    text = tmp[0]
    money = float(tmp[1].replace(",","."))
    trans = {
        "time": str(time.strftime("%Y-%m-%d---%H:%M:%S")),
        "text": text,
        "value": money,
        "by": user_id
    }
    #summary = ""
    for i in range(2,tmp.__len__()):
        result = MONGO.zt_users.update_one({"nick": tmp[i]}, {"$inc": {"value": money}, "$push": {"money": trans}})
        if result.acknowledged is False:
            raise Exception("mongo update")
        #result = MONGO.zt_users.find_one({"nick": tmp[i]})
        #summary += "User: %s | %s \n" % (tmp[i], result['value'])
    #return summary


def show(nick):
    result = MONGO.zt_users.find_one({"nick": nick})
    return result


def show_many(value):
    names = value.split(";")
    text = ""
    for i in names:
        data = show(i)
        if data is not None:
            text += MSG_SHOW_USER % (data['nick'], data['value'])
    return text


def show_users():
    result = MONGO.zt_users.find()
    users = []
    for i in result:
        users.append(i['nick'])
    return users


def show_all():
    users = show_users()
    text = ""
    for i in users:
        text += ";" + i
    return show_many(text)


def show_detail(value):
    names = value.split(";")
    text = ""
    for i in names:
        data = show(i)
        text += "%s: %s&#128; \n" % (data['nick'], data['value'])
        x = data['money'].__len__()
        j = 1
        while ((x - j) >= 0 and j < 5):
            text += MSG_SHOW_MONEY % (data['money'][x - j]['text'], data['money'][x - j]['value'])
            j += 1
        text += "\n"
    return text


def register(chat_id, user_id, user_data, value):
    user = get_user(value)
    if user is not None:
        id = user['id']
    else:
        bot.sendMessage(chat_id, MSG_UNKNOWN_USER)
        return 0
    if user.get("msg_id","") is not "":
        bot.sendMessage(chat_id, MSG_STILL_WAITING_REGISTR)

    keyboard = []
    for i in range(0,6):
        keyboard.append(InlineKeyboardButton(text="Level " + str(i), callback_data=str(i) + ";" + id + ";" + chat_id))
    keyboard.append(InlineKeyboardButton(text="Decline", callback_data="-;" + id + ";" + chat_id))

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [keyboard[0], keyboard[1], keyboard[2], keyboard[3]],
        [keyboard[4], keyboard[5], keyboard[6]]
    ])
    name = user_data.get("first_name", "fn") + " " + user_data.get("last_name", "ln")
    bot.sendMessage(chat_id, "Asking ADMIN for Permissions...")
    sent = bot.sendMessage(zt_chat, "%s asking for registration" % name, reply_markup=keyboard)
    msg_id = telepot.message_identifier(sent)
    update = {
        "msg_id_0": msg_id[0],
        "msg_id_1": msg_id[1],
        "_name": name,
        "_user_id": user_data.get("id", "id")
    }
    MONGO.zt_users.update_one({"id": id}, {"$set": update})


def command(msg, chat_id):
    tmp = msg['text'][1:].split(" ", 1)
    order = tmp[0].lower()
    if tmp.__len__() > 1:
        value = tmp[1]
    else:
        value = None

    chat_id = str(chat_id)
    user_id = str(msg['from']['id'])

    user = user_get(int(user_id))

    if user is not None:
        permission = int(user['permission'])
    else:
        permission = 0

    if order == "register":
        bot.sendMessage(chat_id, MSG_DEPRECATED)
        return 0
        # if user is not None:
        #     bot.sendMessage(chat_id, MSG_ALLREADY_USER)
        #     return 0
        # register(chat_id, user_id, msg['from'], value)
    elif order == "help":
        text = ""
        for i in MSG_COMMANDS:
            text += "%s\t\t\t%s\n" % (i[0], i[1])
        bot.sendMessage(chat_id, text)
    elif order == "show" and permission >= 2:
        result = show_many(value)
        if result is "":
            bot.sendMessage(chat_id, MSG_UNKNOWN_USER)
        else:
            bot.sendMessage(chat_id, result, parse_mode="html")
    elif order == "showhistory" and permission >= 2:
        result = show_detail(value)
        if result is "":
            bot.sendMessage(chat_id, MSG_UNKNOWN_USER)
        else:
            bot.sendMessage(chat_id, result, parse_mode="html")
    elif order == "showall" and permission >= 2:
        bot.sendMessage(chat_id, show_all(), parse_mode="html")
    elif order == "add" and permission >= 3 and value is not None:
        bot.sendMessage(chat_id, add(chat_id, user_id, value))
    elif order == "adduser" and permission >=4 and value is not None:
        if user_add(value, user_id) is 0:
            bot.sendMessage(chat_id, "User %s created" % value)
        else:
            bot.sendMessage(chat_id, "Couldn't create User ... does the acc already exist?")
    elif order == "register_user_answer" and permission >=5 and value is not None:
        #TODO DEV
        bot.sendMessage(chat_id, MSG_IN_DEV)
    return 0


def handle(msg):
    print msg
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'text':
        if msg['text'][0] == '/':
            command(msg, chat_id)


def callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    data = query_data.split(";")
    # answer;id;chat_id
    user_register(permission=data[0], id=data[1])
    if data[0] == '-':
        bot.sendMessage(data[2], "Your request have been rejected!")
    else:
        bot.sendMessage(data[2], MSG_NEW_PERMISSION % (data[0]))



bot.message_loop({'chat': handle, 'callback_query': callback_query})
print "Listen..."

while 1:
    time.sleep(10)

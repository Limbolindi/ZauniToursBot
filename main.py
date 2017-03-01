#!/usr/bin/env python
# -*- coding: utf-8-*-

import ConfigParser
import argparse
from pymongo import MongoClient
from money import Money
from chat import Chat
from data import MSG
import telepot
import json
import time

mongodb_data = None
mongodb_chat = None
bot = None
debug = False

money = None
chat = None


def __init__(conf):
    config = ConfigParser.ConfigParser()
    config.readfp(conf)
    try:
        # setting up the bot
        token = config.get('api', 'token')
        global bot
        bot = telepot.Bot(token)

        # admin = config.get('user', 'admin')
        # admin_chat = config.get('user', 'chat')

        # setting up MongoDB
        client = MongoClient(config.get('mongo', 'ip'), config.getint('mongo', 'port'))
        db = client[config.get('mongo', 'db')]
        if config.getboolean('mongo', 'auth'):
            print 'MongoDB Authentication'
            db.authenticate(raw_input('Username:'), raw_input('Password:'))

        mongodb_data = db[config.get('mongo', 'collection_data')]
        mongodb_chat = db[config.get('mongo', 'collection_chat')]

        global debug
        debug = config.getboolean('settings', 'debug')

        # history_length = config.getint('init', 'history')

        global money
        money = Money(mongodb_data)
        global chat
        chat = Chat(mongodb_data, mongodb_chat)

    except:
        import traceback
        traceback.print_exc()

def command(msg, chat_id):
    tmp = msg['text'][1:].split(" ", 1)
    order = tmp[0].lower()
    if tmp.__len__() > 1:
        value = tmp[1]
    else:
        value = ""

    chat_id = str(chat_id)
    user_id = str(msg['from']['id'])
    user = money.user_get_by_uid(user_id)
    if user is not None:
        permission = int(user['permission'])
    else:
        return 0

    if order == "help" and permission >= 1:
        text = ""
        for i in money.function:
            text += i[2] + "\t\t" + i[3] + "\t\r\n"
        bot.sendMessage(chat_id, text, parse_mode="html")
        return 0

    for k in range(0, money.function.__len__()):
        if money.function[k][1] == order:
            if permission >= money.function[k][4]:
                ret = money.function[k][0](money, value, user_id)
                bot.sendMessage(chat_id, ret, parse_mode="html")
            else:
                if debug:
                    print(user_id, money.function[k][0])
            break
    if chat.keyboard[1] == order:
        if permission >= chat.keyboard[4]:
            ret = chat.keyboard[0](chat, chat_id, user_id, value)
            bot.sendMessage(chat_id, ret[0], parse_mode="html")
            bot.sendMessage(chat_id, ret[1], reply_markup=ret[2], parse_mode="html")
        else:
            if debug:
                print(user_id, money.function[k][0])
        return 0
    for k in range(0, chat.function.__len__()):
        if chat.function[k][1] == order:
            if permission >= chat.function[k][4]:
                ret = chat.function[k][0](chat, chat_id, user_id, value)
                bot.sendMessage(chat_id, ret, parse_mode="html")
            else:
                if debug:
                    print(user_id, money.function[k][0])
            break
    return 0

def handle(msg):
    if debug:
        print json.dumps(msg, indent=4)
        time.sleep(1)
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'text':
        if msg['text'][0] == '/':
            command(msg, chat_id)
def callback(msg):
    if debug:
        print json.dumps(msg, indent=4)
        time.sleep(1)

if __name__ == "__main__":
    #TODO description
    parser = argparse.ArgumentParser(description='description')
    required = parser.add_argument_group("required arguments")
    required.add_argument('conf', help='configfile', type=file)
    args = parser.parse_args()
    __init__(args.conf)

    bot.message_loop({'chat': handle, 'callback_query': callback})
    print "Listen..."
    while 1:
        time.sleep(10)
















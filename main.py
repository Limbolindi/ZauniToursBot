#!/usr/bin/env python
# -*- coding: utf-8-*-

import ConfigParser
import argparse
from pymongo import MongoClient
from user import Money
import telepot
import time
from cars import Chat

mongodb_data = None
mongodb_car = None
bot = None
debug = False

money = None
chat = None

def command(msg, chat_id):
    tmp = msg['text'][1:].split(" ", 1)
    order = tmp[0].lower()
    if tmp.__len__() > 1:
        value = tmp[1]
    else:
        value = None

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
                ret = money.function[k][0](value=value, user_id=user_id)
                bot.sendMessage(chat_id, ret, parse_mode="html")
            else:
                if debug:
                    print(user_id, money.function[k][0])
                pass
            break
    if order == "set":
        bot.sendMessage(chat_id,chat.set_chat(chat_id), parse_mode="html")
    elif order == "s":
        bot.sendMessage(chat_id, chat.show(chat_id), parse_mode="html")
    return 0

def handle(msg):
    if debug:
        print msg
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'text':
        if msg['text'][0] == '/':
            command(msg, chat_id)


if __name__ == "__main__":
    #TODO description
    parser = argparse.ArgumentParser(description='description')
    required = parser.add_argument_group("required arguments")
    required.add_argument('conf', help='configfile', type=file)
    args = parser.parse_args()

    config = ConfigParser.ConfigParser()
    config.readfp(args.conf)

    try:
        # setting up the bot
        token = config.get('api', 'token')
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
        mongodb_car = db[config.get('mongo', 'collection_car')]

        debug = config.getboolean('settings', 'debug')

        # history_length = config.getint('init', 'history')

        money = Money(mongodb_data)
        chat = Chat(mongodb_car)

        bot.message_loop({'chat': handle})
        print "Listen..."
        while 1:
            time.sleep(10)


    except:
        import traceback
        traceback.print_exc()
















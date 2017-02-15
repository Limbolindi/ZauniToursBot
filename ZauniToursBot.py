#!/usr/bin/env python
# -*- coding: utf-8-*-

import ConfigParser
import argparse
from pymongo import MongoClient
import os
import telepot
import json
import time
from decimal import Decimal
import hashlib


BOT = None

GLOBAL = {
    'admin_chat': '',
    'admin_id': '',
    'mongodb': None,
    'debug': False,
    'history': 5

}

EURO = "€".decode("utf-8")

MSG = {
    'show_user': "%s: %s" + EURO + " \n",
    'unknown_nick': "User %s is unknown. \n",
    'missing_param_user': "No username to show. Parameter username is missing! \n",
    'show_history': "\t\t\t\t%s : %s" + EURO + "\n",
    'update_success': "",
    'missing_arguments_add': "missing arguments!\nadd text;value;user1(;user2;userX)\n",
    'user_exists': "User %s already exists\n",
    'user_created': "%s created\n",
    'description': "Programm Beschreibung"


}

COMMANDS = [
    # command , description, permission-level
    ["/help", "prints this help-msg", 1],
    ["/show user1(;user2;userX)", "shows information about user1 optional: (;user2;user3)", 2],
    ["/showall", "information about ALL users: VALUE != 0", 2],
    ["/showall!", "information about ALL users", 2],
    ["/showhistory user1(;user2;userX)", "user-information, including history", 3],
    ["/showdetail user1", "prints ALL information about one user", 3],
    ["/add text;value;user1(;user2;userX)", "add <value> to userX with the kontext: text", 4],
    ["/adduser user1(;user2;userX)", "adds a new User to DB with username = userX", 5]
]


def user_get_by_uid(user_id):
    return GLOBAL['mongodb'].find_one({"user_id": user_id})


def user_get_by_nick(nick):
    return GLOBAL['mongodb'].find_one({"nick_lower": str(nick).lower()})


def show(value, ignore0=False):
    if value is None:
        return MSG['missing_param_user']
    names = value.split(";")
    text = ""
    for i in names:
        print i
        data = user_get_by_nick(i)
        if data is not None:
            if ignore0 and data['value'] == 0.0:
                continue
            text += MSG['show_user'] % (data['nick'], Decimal(data['value'])/Decimal(10))
        else:
            text += MSG['unknown_nick'] % i
    return text


def show_detail(value):
    #TODO overflow too many users?
    if value is None:
        return MSG['missing_param_user']
    names = value.split(";")
    text = ""
    for i in names:
        data = user_get_by_nick(i)
        if data is not None:
            text += json.dumps(data, indent=4)
            text += "\n\n\n"
        else:
            text += MSG['unknown_nick'] % i
    return text


def show_all_users():
    result = GLOBAL['mongodb'].find()
    users = []
    for i in result:
        if i.get("nick", "") is "":
            continue
        users.append(i['nick'])
    users.sort()
    return users


def show_all(ignore0=False):
    users = show_all_users()
    text = ""
    for i in users:
        text += i + ";"
    return show(text[:-1], ignore0)


def show_history(value):
    if value is None:
        return MSG['missing_param_user']
    names = value.split(";")
    text = ""
    for i in names:
        data = user_get_by_nick(i)
        if data is not None:
            text += MSG['show_user'] % (data['nick'], Decimal(data['value'])/Decimal(10))
            x = data['money'].__len__()
            j = 1
            while ((x - j) >= 0 and j < 5):
                text += MSG['show_history'] % (data['money'][x - j]['text'],
                                               Decimal(data['money'][x - j]['value'])/Decimal(10))
                j += 1
            text += "\n"
        else:
            text += MSG['unknown_nick'] % i
    return text


def add(user_id, value):
    tmp = value.split(";")
    if tmp.__len__() < 3:
        return MSG['missing_arguments_add']
    # text;value;user
    text = tmp[0]
    money = int(Decimal(tmp[1].replace(",","."))*10)
    trans = {
        "time": str(time.strftime("%Y-%m-%d")),  #%H:%M:%S
        "text": text,
        "value": money,
        "by": user_id
    }
    ret = ""
    for i in range(2,tmp.__len__()):
        result = GLOBAL['mongodb'].find_one({"nick_lower": str(tmp[i]).lower()})
        if result is None:
            ret += MSG['unknown_nick'] % i
        else:
            result = None
            result = GLOBAL['mongodb'].update_one({"nick_lower": str(tmp[i]).lower()},
                                              {"$inc": {"value": money}, "$push": {"money": trans}})
            if result.acknowledged is False:
                raise Exception("mongo update")
            else:
                ret += MSG['update_success']
    return ret


def add_user(value, user_id):
    if value is None:
        return MSG['missing_param_user']
    nick = value.split(";")
    money = {
        "time": str(time.strftime("%Y-%m-%d")),
        "text": "&lt;start&gt;",
        "value": 0,
        "by": user_id
    }
    text = ""
    for i in nick:
        if GLOBAL['mongodb'].find_one({"nick_lower":str(i).lower()}) is not None:
            text += MSG['user_exists'] % i
        else:
            id = hashlib.sha256(json.dumps(money) + i).hexdigest()[:16]
            result = GLOBAL['mongodb'].update_one({"id": id}, {"$set": {"nick": i, "nick_lower": str(i).lower(),
                                                                        "value": 0, "money": [money]}}, upsert=True)
            if result.raw_result["ok"] is not 1 or result.acknowledged is False:
                raise Exception("mongo update")
            else:
                text += MSG['user_created'] % i
    return text


def command(msg, chat_id):
    tmp = msg['text'][1:].split(" ", 1)
    order = tmp[0].lower()
    if tmp.__len__() > 1:
        value = tmp[1]
    else:
        value = None

    chat_id = str(chat_id)
    user_id = str(msg['from']['id'])

    user = user_get_by_uid(user_id)

    if user is not None:
        permission = int(user['permission'])
    else:
        return 0

    if order == "help" and permission >= 1:
        text = ""
        for i in COMMANDS:
            text += "%s \t\t %s \n\n" %(i[0], i[1])
        BOT.sendMessage(chat_id, text)
    elif order == "show" and permission >= 2:
        BOT.sendMessage(chat_id, show(value), parse_mode="html")
    elif order == "showall!" and permission >= 2:
        BOT.sendMessage(chat_id, show_all(), parse_mode="html")
    elif order == "showall" and permission >= 2:
        BOT.sendMessage(chat_id, show_all(True), parse_mode="html")
    elif order == "showhistory" and permission >= 3:
        BOT.sendMessage(chat_id, show_history(value), parse_mode="html")
    elif order == "showdetail" and permission >= 3:
        BOT.sendMessage(chat_id, show_detail(value), parse_mode="html")
    elif order == "add" and permission >= 4:
        BOT.sendMessage(chat_id, add(user_id, value), parse_mode="html")
    elif order == "adduser" and permission >= 5:
        BOT.sendMessage(chat_id, add(user_id, value), parse_mode="html")


def handle(msg):
    if GLOBAL['debug']:
        print msg
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'text':
        if msg['text'][0] == '/':
            command(msg, chat_id)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=MSG['description'])

    required = parser.add_argument_group("required arguments")
    required.add_argument('conf', help='configfile', type=file)
    parser.add_argument("-i", metavar="NAMES", dest="namefile", type=file,  help='names list\n')
    parser.add_argument("-v", metavar="VALUES", dest="valuefile", type=file, help='value list\n')

    args = parser.parse_args()

    config = ConfigParser.ConfigParser()
    config.readfp(args.conf)

    try:
        # setting up the server
        token = config.get('api', 'token')
        BOT = telepot.Bot(token)

        GLOBAL['admin_chat'] = config.get('user', 'chat')
        GLOBAL['admin_id'] = config.get('user', 'admin')

        # setting up MongoDB
        client = MongoClient(config.get('mongo', 'ip'), config.getint('mongo', 'port'))
        db = client[config.get('mongo', 'db')]
        if config.getboolean('mongo','auth'):
            print 'MongoDB Authentication'
            db.authenticate(raw_input('Username:'), raw_input('Password:'))
        GLOBAL['mongodb'] = db[config.get('mongo', 'collection')]

        GLOBAL['debug'] = config.getboolean('settings','debug')

        GLOBAL['history'] = config.getint('init','history')




        if args.namefile is not None:
            data = list(args.namefile.readlines())
            for i in range(0, data.__len__()-1):
                if data[i][0] is "#":
                    data.pop(i)
            for i in data:
                print add_user(str(i).replace("\n", ""), user_id="000000")

        if args.valuefile is not None:
            data = list(args.valuefile.readlines())
            for i in data:
                tmp = i.replace("\n","").replace("€","").split(";")
                print add("00000", "übertrag aus Liste;" + tmp[0] + ";" + tmp[1])


        for i in config.items("user"):
            if str(i[0])[:4] == "user":
                tmp = i[1].split(",")
                GLOBAL['mongodb'].update_one({"user_id": str(tmp[0])},
                                             {"$set": {"permission": str(tmp[1]), "name": str(tmp[2])}},
                                             upsert=True)



        BOT.message_loop({'chat': handle})
        print "Listen..."

        while 1:
            time.sleep(10)

    except:
        import traceback
        traceback.print_exc()


#!/usr/bin/env python
# -*- coding: utf-8-*-

import ConfigParser
import argparse
#import os
#import json
import time
#import sys
import telepot
import __builtin__
from pymongo import MongoClient


class BgColors:
    def __init__(self):
        pass
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[43m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def __init__(conf):
    config = ConfigParser.ConfigParser()
    config.readfp(conf)
    try:
        # setting up the bot
        token = config.get('api', 'token')
        global bot
        bot = telepot.Bot(token)

        __builtin__.ADMIN = config.get('user', 'admin')
        # admin_chat = config.get('user', 'chat')

        # setting up MongoDB
        client = MongoClient(config.get('mongo', 'ip'), config.getint('mongo', 'port'))
        db = client[config.get('mongo', 'db')]
        if config.getboolean('mongo', 'auth'):
            print 'MongoDB Authentication'
            db.authenticate(raw_input('Username:'), raw_input('Password:'))

        __debug = config.getboolean('settings', 'debug')
        __builtin__.DEBUG = __debug

        from cmd import CommandClass
        __builtin__.CMD = CommandClass(bot)

        # Users
        from modules.users import UsersClass
        __builtin__.USERS = UsersClass(db[config.get('users','collection')], db[config.get('money','collection')])
        return 0

    except:
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='description')
    required = parser.add_argument_group("required arguments")
    required.add_argument('conf', help='configfile', type=file)
    args = parser.parse_args()
    ret = __init__(args.conf)
    if ret is 0:
        bot.message_loop({'chat': CMD.handle, 'callback_query': CMD.callback})
        print "Listen..."
        while 1:
            time.sleep(10)
    else:
        exit(ret)









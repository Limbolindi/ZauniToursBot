#!/usr/bin/env python
# -*- coding: utf-8-*-

from pymongo import MongoClient
import pymongo

EURO = "€".decode("utf-8")
MSG = {
    'adduser_missing_param': "Missing parameter: /adduser username",
    'user_exists_already': "User %s already exists, can't create duplicate!",
    'user_created': "User %s created",
    'error_mongo_adduser': "CRIT _ ERROR _ %s",

    'show_missing_param': "Missing parameter: username",
    'show_user_short': "%s: %s" + EURO + " \n",
    'unknown_username': "User %s is unknown!",
    'show_history': "\t\t\t\t%s : %s" + EURO + "\n",

    'add_missing_param': "Missing arguments: /add text;value;user",
    'error_mongo_add': "CRIT _ ERROR _ %s",
    'add_update_success': "%s set from %s" + EURO + " to %s" + EURO,

    'trans_missing_param': "Missing arguments: /trans text;value;fromUser1;toUser2",
    'chat_already_exists': "",
    'error_mongo_setchat': "%s",
    'chat_created': "%s",
    'unknown_chat': "%s",
    'car_not_found': "%s, %s",
    'car_wrong_seat': "%s",
    'seat_blocked': "%s",
    'select_seat': "choose seat"

}

COMMANDS = [
    # command , description, permission-level
    ["/help", "prints this help-msg", 1],
    ["/register nickname", "register account to use advanced functions, nick is provided by admin", 1],
]

CAR = {
    "head": u"\u2b06\ufe0f\u25ab\ufe0f1\u20e32\u20e33\u20e3\u25ab\ufe0f\n",
    "wall": u"\u25ab\ufe0f\u2b1b\ufe0f\u2b1b\ufe0f\u2b1b\ufe0f\u2b1b\ufe0f\u2b1b\ufe0f\n",
    "A": u"\ud83c\udd70\u2b1b\ufe0f%s\u2b1c\ufe0f%s\u2b1b\ufe0f\n",
    "B": u"\ud83c\udd71\u2b1b\ufe0f%s%s%s\u2b1b\n",
    "back": u"\ud83c\udd91\u2b1b\ufe0f\ud83d\udec4\ud83d\udec4\ud83d\udec4\u2b1b\ufe0f\n",
    "space": u"\u25ab\ufe0f\u2b1b\ufe0f\u2b1c\ufe0f\u2b1c\ufe0f\u2b1c\ufe0f\u2b1b\ufe0f\n",
    "check": u"\u2705",
    "cross": u"\u274c",
    "gray": u"\u2b1c",
    "ghost": u"\U0001f47b"
}

class Struckt():
    mongodb = None

    def __init__(self, mongodb):
        """
        :type mongodb: pymongo.collection.Collection
        """
        if type(mongodb) is not pymongo.collection.Collection:
            raise TypeError(type(mongodb))
        self.mongodb = mongodb

    def user_get_by_uid(self, user_id):
        return self.mongodb.find_one({"user_id": user_id})

    def user_get_by_nick(self, nick):
        return self.mongodb.find_one({"nick_lower": str(nick).lower()})

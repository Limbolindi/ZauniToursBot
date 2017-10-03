#!/usr/bin/env python
# -*- coding: utf-8-*-

EURO = "€".decode("utf-8")

MSG = {
    'adduser_missing_param': "Missing parameter: /adduser username",
    'user_exists_already': "User %s already exists, can't create duplicate!",
    'user_created': "User %s created",
    'error_mongo_adduser': "CRIT _ ERROR _ %s",

    'show_missing_param': "Missing parameter: username",

    'unknown_username': "User %s is unknown!",


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
    'select_seat': "choose seat",

    #new

    'mongo_update_error': 'mongo_update_error',
    'wrong_args': "'%s' is not as expected",
    'show': "%s: %s" + EURO + " \n",
    'history': "\t\t[%s] %s : %s" + EURO + "\n",
    'history_T': "\t\t[%s] %s : %s" + EURO + "\n",
    'all_users': "Users:\n",
    'user1_missing': "user1_missing",
    'user2_missing': "user2_missing",
    'user_exists': 'user_exists',
    'missing_nick': 'missing_nick',
    'missing_uid': 'missing_uid',
    'missing_id': 'missing_id - Identifier',




}

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




class IF(object):
    pass


RET = {
    'cant_find_user': 10,
    #'unknown_user_id': 11,
    #'unknown_nick': 12,
    'missing_nick': 20,
    'missing_id': 23,
    'user_exists': 25,
    'error_trans': 30,
    'nothing_to_write': 32,
}


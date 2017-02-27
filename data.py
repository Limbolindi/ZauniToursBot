#!/usr/bin/env python
# -*- coding: utf-8-*-

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
    'error_mongo_setchat': "",
    'chat_created': "",
    'unknown_chat': "",
    'car_not_found': ""
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
    "cross": u"\u274c"
}
#!/usr/bin/env python
# -*- coding: utf-8-*-

import time
from decimal import Decimal
import json

from data import MSG, Struckt


class Money():

    def __init__(self, database):
        self.money = self.__Money(database)

    def Show(self, value, user_id):
        return self.show(value)

    def Add(self, value, user_id):
        return self.add(value, user_id)

    def Transact(self, value, user_id):
        return self.transact(value, user_id)

    def ShowHistory(self, value, user_id):
        return self.show_history(value)

    def ShowAll(self, value, user_id):
        return self.show_all(True)

    def ShowAllForce(self, value, user_id):
        return self.show_all(True)

    #self, value, user_id
    functions = [
        [Transact,      "trans",        "/trans text;value;fromUser1;toUser2",  "",                                                         8],
        [Add,           "add",          "/add text;value;user1(;user2;userX)",  "add <value> to userX with the kontext: text",              8],
        [ShowHistory,   "history",      "/history user1(;user2;userX)",         "user-information, including history",                      6],
        [ShowAllForce,  "!showall",     "/!showall",                            "information about ALL users",                              6],
        [ShowAll,       "showall",      "/showall",                             "information about ALL users: VALUE != 0",                  6],
        [Show,          "show",         "/show user1(;user2;userX)",            "shows information about user1 optional: (;user2;user3)",   6]
    ]

    class __Money(Struckt):
        '''
        Basic handling of Balance of the Users in the DB
        '''

        def show_all_users_in_db(self):
            '''
            creates a List with all db-users
            :return: <list> with all user-nick's
            '''
            result = self.mongodb.find()
            users = []
            for user in result:
                if user.get("nick", "") is "":
                    continue
                users.append(user['nick'])
            users.sort()
            return users

        def show(self, value, ignore_zero=False):
            """
            Shows basic balance Information about user(s) set in value
            :param value: nickname
            :param ignore_zero: True - ignores Accounts with balance 0.0
            :return: text
            """
            if value is None:
                return MSG['show_missing_param']
            names = value.split(";")
            text = ""
            for nick in names:
                data = self.user_get_by_nick(nick)
                if data is not None:
                    if ignore_zero and data['balance'] == 0.0:
                        continue
                    text += MSG['show_user_short'] % (data['nick'], Decimal(data['balance']) / Decimal(10))
                else:
                    text += MSG['unknown_username'] % nick
            return text

        def show_all(self, ignore_zero=True):
            """
            shows Information (based on show) for every user
            :param ignore_zero: True - ignores balance 0.0
            :return: text
            """
            users = self.show_all_users_in_db()
            text = ""
            for i in users:
                text += i + ";"
            return self.show(text[:-1], ignore_zero)

        def show_history(self, value, length = 5):
            """
            show Information + Transaction history
            :param value: usename
            :param length: history length
            :return: text
            """
            if value is None:
                return MSG['show_missing_param']
            names = value.split(";")
            text = ""
            for nick in names:
                data = self.user_get_by_nick(nick)
                if data is not None:
                    text += MSG['show_user_short'] % (data['nick'], Decimal(data['balance']) / Decimal(10))
                    if data.get('money', None) is None:
                        continue
                    x = data['money'].__len__()
                    j = 1
                    while ((x - j) >= 0 and j <= length):
                        text += MSG['show_history'] % (data['money'][x - j]['text'],
                                                       Decimal(data['money'][x - j]['value']) / Decimal(10))
                        j += 1
                    text += "\n"
                else:
                    text += MSG['unknown_username'] % nick
            return text

        def add(self, value, user_id):
            """
            edit balance of user
            :param value: transactionText;mony-value;username
            :param user_id: done by user_id
            :return: text
            """
            tmp = value.split(";")
            if tmp.__len__() < 3:
                return MSG['add_missing_param']
            # text;value;user
            text = tmp[0]
            money = int(Decimal(tmp[1].replace(",", ".")) * 10)
            trans = {
                "time": str(time.strftime("%Y-%m-%d")),  # %H:%M:%S
                "text": text,
                "value": money,
                "by": user_id
            }
            ret = ""
            for i in range(2, tmp.__len__()):
                nick = tmp[i]
                result = self.mongodb.find_one({"nick_lower": str(nick).lower()})
                if result is None:
                    ret += MSG['unknown_username'] % nick
                else:
                    old_balance = result.get("balance",0)
                    result = None
                    result = self.mongodb.update_one({"nick_lower": str(nick).lower()},
                                                          {"$inc": {"balance": money}, "$push": {"money": trans}})
                    if result.acknowledged is False:
                        ret += MSG['error_mongo_add'] % nick
                    else:
                        ret += MSG['update_success'] % (nick, old_balance, old_balance + money)
            return ret

        def transact(self, value, user_id):
            """
            transfer money from user1 to user2
            :param value: text;ammount of Money; user1;user2
            :param user_id: done by user_id
            :return: text
            """
            tmp = value.split(";")
            if tmp.__len__() < 4:
                return MSG['trans_missing_param']
            # text;value;user;user2
            money = int(Decimal(tmp[1].replace(",", ".")))
            result = self.mongodb.find({"nick_lower": str(tmp[2]).lower()})
            if result is None:
                return MSG['unknown_username'] % tmp[2]
            result = self.mongodb.find_one({"nick_lower": str(tmp[3]).lower()})
            if result is None:
                return MSG['unknown_username'] % tmp[3]
            v1 = "[T] " + tmp[0] + ";" + str(money * -1) + ";" + tmp[2]
            v2 = "[T] " + tmp[0] + ";" + str(money) + ";" + tmp[3]
            ret = ""
            ret += self.add(user_id, v1)
            ret += self.add(user_id, v2)
            return ret

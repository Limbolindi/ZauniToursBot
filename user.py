#!/usr/bin/env python
# -*- coding: utf-8-*-

import time
#from pymongo import MongoClient
import pymongo
from decimal import Decimal
import json
import data

from data import MSG



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


class Money(Struckt):

    def show_all_users_in_db(self):
        result = self.mongodb.find()
        users = []
        for user in result:
            if user.get("nick", "") is "":
                continue
            users.append(user['nick'])
        users.sort()
        return users

    def add_user(self, value, user_id):
        if value is None:
            return MSG['adduser_missing_param']
        nicks = value.split(";")
        money = {
            "time": str(time.strftime("%Y-%m-%d")),
            "text": "&lt;start&gt;",
            "value": 0,
            "by": user_id
        }
        text = ""
        for nick in nicks:
            if self.mongodb.find_one({"nick_lower":str(nick).lower()}) is not None:
                text += MSG['user_exists_already'] % nick
            else:
                result =self.mongodb.update_one({"nick": nick}, {"$set": {"nick_lower": str(nick).lower(),
                                                                            "value": 0, "money": [money]}}, upsert=True)
                if result.raw_result["ok"] is not 1 or result.acknowledged is False:
                    text += MSG['error_mongo_adduser'] % nick
                else:
                    text += MSG['user_created'] % nick
        return text

    def show(self, value, user_id=None, ignore_zero=True):
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
        users = self.show_all_users_in_db()
        text = ""
        for i in users:
            text += i + ";"
        return self.show(text[:-1], ignore_zero)

    def show_all_withZ(self, value=None, user_id=None):
        return self.show_all(False)

    def show_all_ignoreZ(self, value=None, user_id=None):
        return self.show_all(True)

    def show_history(self, value, user_id=None):
        if value is None:
            return MSG['show_missing_param']
        names = value.split(";")
        text = ""
        for nick in names:
            data = self.user_get_by_nick(nick)
            if data is not None:
                text += MSG['show_user_short'] % (data['nick'], Decimal(data['balance']) / Decimal(10))
                x = data['money'].__len__()
                j = 1
                while ((x - j) >= 0 and j <= 5):
                    text += MSG['show_history'] % (data['money'][x - j]['text'],
                                                   Decimal(data['money'][x - j]['value']) / Decimal(10))
                    j += 1
                text += "\n"
            else:
                text += MSG['unknown_username'] % nick
        return text

    def show_detail(self, value, user_id=None):
        if value is None:
            return MSG['show_missing_param']
        nick = value.split(";")[0]
        data = self.user_get_by_nick(nick)
        if data is not None:
            return json.dumps(data, indent=4)
        else:
            MSG['unknown_username'] % nick

    def add(self, value, user_id):
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
        tmp = value.split(";")
        if tmp.__len__() < 4:
            return MSG['trans_missing_param']
        # text;value;user;user2
        money = int(Decimal(tmp[1].replace(",", ".")))
        result = self.mongodb.find({"nick_lower": str(tmp[2]).lower()})
        if result is None:
            return MSG['unknown_username'] % tmp[2]
        result = None
        result = self.mongodb.find_one({"nick_lower": str(tmp[3]).lower()})
        if result is None:
            return MSG['unknown_username'] % tmp[3]
        v1 = "[T] " + tmp[0] + ";" + str(money * -1) + ";" + tmp[2]
        v2 = "[T] " + tmp[0] + ";" + str(money) + ";" + tmp[3]
        ret = ""
        ret += self.add(user_id, v1)
        ret += self.add(user_id, v2)
        return ret

    function = [
        [add_user,      "adduser",      "/adduser user1(;user2;userX)", "adds a new User to DB with username = userX",                     10],
        [transact,      "trans",        "/trans text;value;fromUser1;toUser2", "",                                                          8],
        [add,           "add",          "/add text;value;user1(;user2;userX)",  "add <value> to userX with the kontext: text",              8],
        [show_detail,   "showdetail",   "/showdetail user1",                    "prints ALL information about one user",                    6],
        [show_history,  "showhistory",  "/showhistory user1(;user2;userX)",     "user-information, including history",                      6],
        [show_all_withZ,"showall!",     "/showall!",                            "information about ALL users",                              6],
        [show_all_ignoreZ,"showall",    "/showall",                             "information about ALL users: VALUE != 0",                  6],
        [show,          "show",         "/show user1(;user2;userX)",            "shows information about user1 optional: (;user2;user3)",   6]
    ]








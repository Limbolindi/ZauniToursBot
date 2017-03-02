#!/usr/bin/env python
# -*- coding: utf-8-*-

import time
from data import Struckt, MSG
import pymongo
from decimal import Decimal


class Users(object):

    def __init__(self, database):
        self.users = self.__Users(database)

    def NewUser(self, nick, balance = 0, text= None):
            return self.users.new(nick, balance, text)

    def GetUser(self, user_id = None, nick = None):
        if not nick and not user_id:
            return MSG.get('missing_id', 'missing_id')
        if nick:
            return self.users.get_by_nick(nick)
        elif user_id:
            return self.users.get_by_uid(user_id)
        return MSG.get('missing_uid', 'missing_uid')

    def ShowAll(self):
        return self.users.showall(False)

    def ShowAllForce(self):
        return self.users.showall(True)

    def Transaction(self, nick1, nick2, value, text):
        return self.users.transaction(nick1=nick1, nick2=nick2, value=value, text=text)

    commands = [
        (NewUser, "newuser"),
        (ShowAll, "showall"),
        (ShowAllForce, "!showall"),
        (Transaction, "trans")
    ]


    class __Users(Struckt):
        """
        Handling all tasks about Users
        """

        def __get_user(self, user):
            if user is None:
                return None

            return User(
                database= self.mongodb,
                nick= user.get("nick", None),
                balance= user.get("balance", None),
                money= user.get("money", None),
                permission= user.get("permission", None),
                user_id= user.get("user_id", None),
                name= user.get("name", None)
            )

        def get_by_uid(self, user_id):
            return self.__get_user(self.mongodb.find_one({"user_id": user_id}))

        def get_by_nick(self, nick):
            return self.__get_user(self.mongodb.find_one({"nick_lower": str(nick).lower()}))

        def new(self, nick, balance, text):
            if not nick:
               return MSG.get('missing_nick','missing_nick')
            if self.get_by_nick(nick):
                return MSG.get('user_exists', 'user_exists')
            user = User(database=self.mongodb, nick=nick, new=True)
            if text:
                user.Transaction(text= text, value= balance)
            elif balance != 0:
                user.Transaction(text="init", value=balance)
            return user.Write()

        def showall(self, force):
            data = [u.get("nick","") for u in self.mongodb.find()]
            data.sort()
            all = [self.get_by_nick(n) for n in data]
            data = []
            if force:
                data = [ i.Show() for i in all]
            else:
                for i in all:
                    if i.GetBalance():
                        data.append(i.Show())

            text = MSG.get('all_users', 'all_users')
            for d in data:
                text += "\n" + d
            return text

        def transaction(self, nick1, nick2, value, text):
            nick1 = self.get_by_nick(nick1)
            if not nick1:
                return MSG.get('user1_missing', 'user1_missing')
            nick2 = self.get_by_nick(nick2)
            if not nick2:
                return MSG.get('user2_missing', 'user2_missing')
            value = int(Decimal(str(value).replace(",", ".")) * 100)
            nick1.Transaction(text=text, value=(Decimal(value * -1) / Decimal(100)), user=nick2.GetNick())
            nick2.Transaction(text=text, value=(Decimal(value) / Decimal(100)), user=nick1.GetNick())
            return 0

class User(object):

    def __init__(self, database, nick=None, balance=0, money=None, permission=None, name=None, user_id=None, new=False):
        self.user = self.__User(database=database, nick=nick, balance=balance, money=money, permission=permission, name=name, user_id=user_id, new=new)

    def Write(self):
        if self.user.new:
            return self.user.write()
        return 0

    def Show(self):
        return self.user.show(0, False)

    def Transaction(self, text, value, user=None):
        self.user.new_transaction(text, value, user)
        return self.user.write()

    def GetBalance(self):
        return int(Decimal(self.user.balance) / Decimal(100))

    def GetNick(self):
        return self.user.nick

    def ShowData(self, lenght=5):
        return self.user.show(lenght, False)

    commands = [
        (Show, "showuser"),
        (Transaction, "add"),
        (ShowData, "history")
    ]

    class __User(object):

        def __init__(self, database, nick, balance, money, permission, name, user_id, new):
            if type(database) is not pymongo.collection.Collection:
                raise TypeError(type(database))
            self.mongodb = database

            if not nick or len(nick) is not 9:
                raise Exception(MSG.get('wrong_args',"%s wrong") % "nick")
            self.nick = nick

            if balance is None or type(balance) is not int:
                raise Exception(MSG.get('wrong_args',"%s wrong") % "balance")
            self.balance = balance

            if money and type(money) is not list:
                raise Exception(MSG.get('wrong_args',"%s wrong") % "money")
            self.money = money

            if permission and type(permission) is not int:
                raise Exception(MSG.get('wrong_args',"%s wrong") % "permission")
            self.permission = permission

            self.name = name
            self.user_id = user_id
            self.new = new

        def __get_dict(self):
            u = {
                "nick": self.nick,
                "nick_lower": str(self.nick).lower(),
                "balance": self.balance
            }
            if self.money:
                u["money"] = self.money
            if self.name:
                u["name"] = self.name
            if self.permission:
                u["permission"] = self.permission
            if self.user_id:
                u["user_id"] = self.user_id
            return u

        @staticmethod
        def __get_value(value):

            try:
                return int(Decimal(str(value).replace(",", ".")) * 100)
            except:
                raise TypeError(value)

        def new_transaction(self, text, value, user=None, type="N"):
            if not text or not value:
                raise Exception(MSG.get('wrong_args',"%s wrong") % "text|value")
            m = {
                "text": text,
                "value": self.__get_value(value),
                "time": str(time.strftime("%Y-%m-%d")),
                "type": type
            }
            if user:
                m["type"] = "T"
                m["user"] = user
            if not self.money:
                self.money = [m]
            else:
                self.money.append(m)
            self.balance += self.__get_value(value)
            return 0

        def write(self):
            result = self.mongodb.update_one(
                {"nick": self.nick},
                {"$set": self.__get_dict()},
                upsert=self.new
            )
            if result.raw_result["ok"] is not 1 or result.acknowledged is False:
                raise Exception(MSG.get('mongo_update_error', 'mongo_update_error'))
            self.new = False
            return 0

        def show(self, length, details):
            text = MSG.get('show', '%s - %s') % (self.nick, ( Decimal(self.balance) / Decimal(100) ) )
            if length and self.money:
                i = len(self.money) -1
                while ( i >= 0 and length >= 0):
                    if self.money[i].get("type","X") == "T":
                        text += MSG.get('history_T', '[%s] - %s - %s') % (
                            self.money[i].get("user", "user_X"),
                            self.money[i].get("text", "-txt-"),
                            (Decimal(self.money[i].get("balance", 0)) / Decimal(100))
                        )
                    else:
                        text += MSG.get('history', '[%s] - %s - %s') % (
                            self.money[i].get("type","X"),
                            self.money[i].get("text","-txt-"),
                            ( Decimal(self.money[i].get("balance",0)) / Decimal(100) )
                        )
                text += "\n\n"
            if details:
                pass

            return text










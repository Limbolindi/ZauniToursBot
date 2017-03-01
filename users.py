#!/usr/bin/env python
# -*- coding: utf-8-*-

from data import Struckt, MSG


class Users:

    def __init__(self, database):
        self.users = self.__Users(database)

    def AddUser(self, value, user_id):
        return self.users.add_user(value)

    functions = [
        [AddUser,   "adduser",  "/adduser username",    "",     10]
    ]


    class __Users(Struckt):
        """
        Handling all tasks about Users
        """

        def add_user(self, value):
            """
            adds a new user to database.
            :param value: username
            :return: msg
            """
            if value is None:
                return MSG['adduser_missing_param']
            nicks = value.split(";")
            text = ""
            for nick in nicks:
                if self.mongodb.find_one({"nick_lower": str(nick).lower()}) is not None:
                    text += MSG['user_exists_already'] % nick
                else:
                    result = self.mongodb.update_one({"nick": nick}, {"$set": {"nick_lower": str(nick).lower(),
                                                                               "balance": 0}}, upsert=True)
                    if result.raw_result["ok"] is not 1 or result.acknowledged is False:
                        text += MSG['error_mongo_adduser'] % nick
                    else:
                        text += MSG['user_created'] % nick
            return text



#!/usr/bin/env python
# -*- coding: utf-8-*-


from data import Struckt

class Users(Struckt):
    # [add_user,      "adduser",      "/adduser user1(;user2;userX)", "adds a new User to DB with username = userX",                     10],
    def register(self, user_id, nick):
        pass

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
        # , "money": [money]
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
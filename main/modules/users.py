#!/usr/bin/env python
# -*- coding: utf-8-*-

import pymongo
import json
import time
from main import BgColors

TEXT = {
    'invalid_nick': "No nick or an invalid nick was provided. The nick has to be like: /n VVVV.NNNN",
    'user_in_db': "User [%s] is already in the DB",
    'nothing_show': "Nothing to show. Missing some Arguments or Permissions?"


}
ParsingInfo= [
    ['nick',        ('n', 'nick')],
    ['username',    ('u', 'username', 'user')],
    ['security',    ('s', 'security')],
    ['all',         ('a', 'all')],
    ['history',     ('h', 'history', 'length')],
    ['short',       ('x', 'short')],
    ['text',        ('t', 'txt', 'text')],
    ['value',       ('v', 'e', 'value', 'euro')]
]


class UsersClass(object):
    def __init__(self, database, moneyDB):
        if type(database) is not pymongo.collection.Collection:
            raise TypeError(type(database))
        self.mongodb = database
        self.moneydb = moneyDB
        CMD.add_db_command({
            'funct': self.bot_new_user,
            'keys': ['new', 'new_user', 'add_user'],
            'description': "",
            'params': ['/n nick'],
            'options': ['/u username', '/s int(security)'],
            'name': "new",
            'security': 0,
            'enabled': True
        })
        CMD.add_db_command({
            'funct': self.bot_show_user,
            'keys': ['show', 's'],
            'description': "",
            'params': [],
            'options': ['/u username', '/n nick', '/h int(history)', '/! (short version)'],
            'name': "show",
            'security': 0,
            'enabled': True
        })
        CMD.add_db_command({
            'funct': self.bot_show_user_self,
            'keys': ['self'],
            'description': "",
            'params': [],
            'options': ['/h int(history)', '/! (short version)'],
            'name': "self",
            'security': 0,
            'enabled': True
        })
        CMD.add_db_command({
            'funct': self.bot_money_add,
            'keys': ['add', 'a'],
            'description': "",
            'params': ['/v value', '/t text', '/u username | /n nick'],
            'options': [],
            'name': "add money",
            'security': 0,
            'enabled': True
        })

    # ### new user ### #
    def bot_new_user(self, msg, data, user_security):
        return self.__new_user(self.__pars_args(data))

    def bot_r_new_user(self, msg, msg_replay, msg_replayed, user_security):
        # TODO bot_r_new_user()
        return "NOT implemented yet"

    def __new_user(self, data):
        nick = data.get('nick', None)
        # check the nickname if it matches the pattern
        if nick is None or len(nick) != 9 or nick[4:5] != "." or not str(nick[:4] + nick[5:]).isalpha():
            return TEXT['invalid_nick']

        user = self.__get_user_by_nick(nick)
        if user[0]:
            return [TEXT['user_in_db'] % nick]

        user = {
            'nick': data.get('nick'),
            'nick_l': str(data.get('nick')).lower(),
        }

        if data.get('security', None).strip().isdigit():
            user['security'] = int(data.get('security').strip())
        else:
            user['security'] = 0

        # # user # #
        if 'username' in data:
            if str(data.get('username')).strip().lower()[0:1] == "@":
                user['username'] = str(data.get('username')).strip().lower()[1:]
            else:
                user['username'] = str(data.get('username')).strip().lower()

        result = self.mongodb.update_one(
            {"nick_l": str(data.get('nick')).lower()},
            {"$set": user},
            upsert=True
        )

        if result.raw_result["ok"] is not 1 or result.acknowledged is False:
            raise Exception("Add to MongoDB-Users %s ERROR" % nick)

        # # money # #
        result = self.moneydb.update_one(
            {"nick": str(data.get('nick')).lower()}, {
                "$set": {
                    "nick": str(data.get('nick')).lower(),
                    "balance": 0
                },
                "$push": {
                    "money": {
                        "time": str(time.strftime("%Y-%m-%d")),
                        "text": '__init__',
                        "value": 0,
                    }
                }
             },
            upsert=True
        )
        if result.raw_result["ok"] is not 1 or result.acknowledged is False:
            raise Exception("Add to MongoDB-Money %s ERROR" % nick)

        return None

    # ### show user ### #
    def bot_show_user_self(self, msg, data, user_security):
        args = self.__pars_args(data)
        if 'username' in args:
            args.pop('username')
        if 'nick' in args:
            args.pop('nick')
        if 'username' in msg.get('from',{}):
            args['username'] = msg.get('from').get('username')
            return self.__show(args)
        else:
            return TEXT['nothing_show']

    def bot_show_user(self, msg, data, user_security):
        args = self.__pars_args(data)
        if ('username' and 'nick') not in args:
            if 'username' in msg.get('from',{}):
                args['username'] = msg.get('from').get('username')
            else:
                return TEXT['nothing_show']
        return self.__show(args)

    def bot_r_show_user(self, msg, msg_replay, msg_replayed, user_security):
        # TODO bot_r_show_user()
        return []

    def __show(self, data):
        users = self.__get_users(data)
        # TODO Format Output 'show'
        result = ""
        history = int(data.get('history', 4))
        for i in users:
            d = {}
            d['Nick'] = i[0]['nick']
            d['Balance'] = i[1]['balance']
            d['Username'] = i[0]['username']
            if 'short'not in data:
                tmp = []
                counter = 0
                while counter < (len(i[1]['money']) and history):
                    print counter
                    tmp.append(i[1]['money'][counter])
                    counter += 1
                # for x in tmp:
                # ToDo Format Show History
                d['history'] = json.dumps(tmp, indent=3)

            for key in d.keys():
                result += str(key) + ": " + str(d[key]) + "\n"
            result += "\n"

        return result

    # ### update user ### #
    def bot_update_user(self, msg, data, user_security):
        # TODO bot_update_user()
        return []

    def bot_r_update_user(self, msg, msg_replay, msg_replayed, user_security):
        # TODO bot_r_update_user()
        return []

    # ### get_user ### #
    def _get(self, header, data):
        user = self.mongodb.find_one({header: data})
        money = None
        if user:
            money = self.moneydb.find_one({'nick': user['nick_l']})
        return (user, money)

    def __get_user_by_nick(self, nick):
        # check the nickname if it matches the pattern
        if nick is None or len(nick) != 9 or nick[4:5] != "." or not str(nick[:4] + nick[5:]).isalpha():
            raise Exception("Invalid NICK")
        return self._get("nick_l", str(nick).lower())

    def __get_user_by_username(self, username):
        return self._get("username", str(username).lower())

    def __get_users(self, data):
        users = []
        if 'username' in data:
            for x in data.get('username').strip().split(" "):
                if x[0:1] == "@":
                    users.append(self.__get_user_by_username(x[1:]))
                else:
                    users.append(self.__get_user_by_username(x))
        if 'nick' in data:
            for x in data.get('nick').strip().split(" "):
                users.append(self.__get_user_by_nick(x))
        return users

    # ### assistance ### #
    @staticmethod
    def __pars_args(data):
        result = {}
        for d in data[1:]:
            for c in ParsingInfo:
                if str(d[0]) in c[1]:
                    result[c[0]] = d[1]
        return result

    @staticmethod
    def __pars_money(data):

        tmp = str(data.strip().replace(',','.').replace(u'\u20ac','').replace('\\u20ac',''))
        if not tmp.replace('.','').isdigit():
            if tmp[0] is ('-' or '+'):
                if not tmp[1:].replace('.', '').isdigit():
                    return None
            else:
                return None
        if tmp.count('.') > 1:
            return None
        value = float(tmp)
        value *= 100
        return int(value)

    # ### send money ### #
    def bot_money_add(self, msg, data, user_security):
        # ToDo bot_money_add()
        args = self.__pars_args(data)

        # # ## value ## # #
        if 'value' not in args:
            # ToDo Error MSG missing value in send
            return "ERROR V"

        tmp = self.__pars_money(args.get('value'))
        if not tmp:
            # ToDo Error MSG missing value
            return "ERROR V PArs"
        args['value'] = int(tmp)

        # # ## nick/users ## # #
        if ('nick' and 'username') not in args:
            # ToDo missing user/nick in send
            return "error U"

        args['users'] = self.__get_users(args)

        # # ## text ## # #
        if 'text' not in args:
            # ToDo error no text in send
            return "error T"

        return self.__send_money(args)

    def bot_r_money_add(self, msg, msg_replay, msg_replayed, user_security):
        # ToDo bot_r_money_add()
        pass

    def bot_money_send(self, msg, data, user_security):
        # ToDo bot_money_send()
        pass

    def __send_money(self, data):
        users = data.get('users')
        transaction = {
            "time": str(time.strftime("%Y-%m-%d")),
            "text": data.get('text'),
            "value": int(data.get('value')),
        }
        returnvalue = []
        for u,m in users:
            if u and m:
                balance = m.get('balance')
                result = None
                result = self.moneydb.update_one({"nick": m.get('nick')},{
                    "$inc": {
                        "balance": int(data.get('value')) },
                    "$push": {"money": transaction}
                })
                if result.acknowledged is False:
                    returnvalue.append(TEXT['send_error'] % (m.get('nick'), balance))
                print BgColors.OKBLUE
                print str("Updated: n: %s from %s to %s. DB: %s" % (
                    m.get('nick'),
                    str(balance),
                    str(data.get('value') + balance),
                    result)
                    )
                print BgColors.ENDC
        return returnvalue

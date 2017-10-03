#!/usr/bin/env python
# -*- coding: utf-8-*-

import time
import pymongo
from decimal import Decimal

TEXT = {
    'unknown_user': "%s   is unknown",
    'add-error': "Something went WRONG! SRY\n Old Balance of User %s was %s (pleas check if correct)",
    'send-error': "Something went WRONG! SRY\n",
    'invalid_nick': "Provided nick \"%s\" has wrong format. Please use: LLLL.FFFF (Lastname, Firstanme).",
    'show-username-missing': "\"show\" needs the Parameter /u <username>",
    'add-nick-missing': "\"add_user\" needs the Parameter /u <nick>",

}


class Class(object):

    def __init__(self, database, data):
        """
            :rtype:  pymongo.collection.Collection
        """
        if type(database) is not pymongo.collection.Collection:
            raise TypeError(type(database))
        self.mongodb = database
        self.history = data.get('history', 4)
        self.users = data.get('class', None)
        if not self.users:
            raise Exception
        self.functions=[]
        self.reply=[]


        #self.functions.append([self.get, True, "get", "blahh Beschreibung", 0])
        #self.functions.append([self.send, True, "add", "blahh Beschreibung", 0])
        #self.functions.append([self.send, True, "money", "blahh Beschreibung", 0])
        #self.functions.append([self.send, True, "send", "blahh Beschreibung", 0])

        #self.reply.append([self.sendTo, True, "add", "blahh Beschreibung", 0])
        #self.reply.append([self.sendTo, True, "money", "blahh Beschreibung", 0])
        #self.reply.append([self.sendTo, True, "send", "blahh Beschreibung", 0])
        self.functions.append({'funct': self.bot_show,
                               'keys': ["show", "s"],
                               'description': "Shows Information about the balance of an user",
                               'usage': "/show /n nick | /u username (/h history-length)",
                               'name': "/show",
                               'security': 17,
                               'enabled': True
                               })
        self.functions.append({'funct': self.bot_add_user,
                               'keys': ["add_user", "new_user", "new"],
                               'description': "Add new User to db",
                               'usage': "/new /n nick ( /u username )",
                               'name': "/new_user",
                               'security': 33,
                               'enabled': True
                               })





    def show(self, nick, history):
        result = ""
        data = self.mongodb.find_one({'nick': nick})
        if data:
            balance = data['balance']
            money = data['money']
            result = "nick:  " + nick + "\n"
            result += "balance: " + str(balance/10.0) + u'\u20ac' + "\n"
            #result += "history:  \n"
            i = 0
            while(i < (history) and (len(money) - i)> 0):
                result += "   [ " + money[i]['text'] + "  "
                result += "" + str(money[i]['value']/10.0) + "  ] "
                #result += "    " + money[i]['time'] + "\n"
                i+=1

        return result









    def bot_send(self, data):
        pass



    #msg + users=[<user>]
    # self, data
    def send(self, data, users, reverse=False):
        value = None
        text = None
        for i in range(1, len(data)):
            if data[i][0] in ('text', 't'):
                text = data[i][1]
            elif data[i][0] in ('value', 'v', 'e', 'euro', 'EURO', u'\u20ac'):
                tmp = data[i][1].replace(u"\u20ac", "")
                tmp = str(tmp.replace(",", "."))
                tmp = tmp.strip()
                if str(tmp.replace(".","",1)).isdigit():
                    value = int(Decimal(tmp) * 100)
                    #if reverse:
                    #    value *= -1
                else:
                    print TEXT.get('send-error')
                    print data
                    return TEXT.get('send-error')
            else:
                pass

        debug({'value':value, 'text': text, 'users':users})
        res = self._send(user=None, value=None, text=None)

    def _send(self, user,  value, text, user_to=None ):

        trans = {
            "time": str(time.strftime("%Y-%m-%d")),
            "text": text,
            "value": value,
        }
        ret = ""
        for f in user:
            result = self.db.find_one({"nick": f})
            if result is None:
                ret += TEXT['add-unknown_user'] % f
            else:
                old_balance = result.get("balance", 0)
                result = None
                result = self.db.update_one({"nick_lower": f},
                                                 {"$inc": {"balance": money}, "$push": {"money": trans}})
                if result.acknowledged is False:
                    ret += TXT['add-error'] % (f, old_balance)
        for t in user_to:
            print t
        return ret



    #TODO show
    def get(self, msg):
        self._get(nick=None)

    def _get(self, nick):
        pass

    #FIXME with @user_add
    def create(self, nick):
        pass
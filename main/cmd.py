#!/usr/bin/env python
# -*- coding: utf-8-*-

import telepot
from main import BgColors


TEXT = {
    'unexpected-error': "Sorry something went wrong -.-"
}


class CommandClass(object):

    def __init__(self, bot):
        self.bot = bot
        self.db_replay = []
        self.db_command = []
        self.db_new_participant = []
        self.db_callback = []

    def add_db_replay(self, db):
        self.db_replay.append(db)

    def add_db_command(self, db):
        self.db_command.append(db)

    def add_db_new_participant(self, db):
        self.db_new_participant.append(db)

    def add_db_callback(self, db):
        self.db_callback.append(db)

    def handle(self, msg):
        try:
            if DEBUG:
                import json
                print BgColors.WARNING
                print json.dumps(msg, indent=4)
                print BgColors.ENDC

            content_type, chat_type, chat_id = telepot.glance(msg)
            # FIXME get user security
            user_security = 0
            if msg.has_key('reply_to_message'):
                self.reply_to_message(msg, chat_id, user_security)
            elif content_type == 'text':
                data = self.__split_msg(msg)
                if data:
                    self.process_command(msg, chat_id, data, user_security)
            elif content_type == 'new_chat_member':
                self.new_participant(msg, chat_id, user_security)
        except:
            import json
            import traceback
            self.bot.sendMessage(ADMIN, json.dumps(msg, indent=4))
            self.bot.sendMessage(ADMIN, traceback.format_exc())
            self.bot.sendMessage(chat_id, TEXT['unexpected-error'])
            traceback.print_exc()

    def callback(self, msg):
        import json
        self.bot.sendMessage(ADMIN, "callback")
        json.dumps(msg, indent=4)

    # ### reply ### #
    def reply_to_message(self, msg, chat_id, user_security):
        msg_replay = msg.copy()
        msg_replay.pop('reply_to_message')
        msg_replay_cmd = self.__split_msg(msg_replay)
        msg_replayed = msg['reply_to_message'].copy()
        msg_replayed_cmd = self.__split_msg(msg_replayed)
        funct = self.__check_reply(msg_replay_cmd[0][0])
        if funct is None:
            return None
        else:
            res = []
            for f in funct:
                if f.get('enabled') and f.get('security') <= user_security:
                    msg_replay['text'] = msg_replay_cmd
                    msg_replayed['text'] = msg_replayed_cmd
                    res.append(f.get('funct')(msg, msg_replay, msg_replayed, user_security))
            self.__response(chat_id, res)

    def __check_reply(self, cmd):
        result = []
        for f in self.db_replay:
            if cmd in f.get("keys"):
                result.append(f)
        return result

    # ### command ### #
    def process_command(self, msg, chat_id, data, user_security):
        funct = self.__check_command(data[0][0])
        if funct is None:
            return None
        else:
            res = []
            for f in funct:
                if f.get('enabled') and f.get('security') <= user_security:
                    res.append(f.get('funct')(msg, data, user_security))
            self.__response(chat_id, res)

    def __check_command(self, cmd):
        result = []
        for f in self.db_command:
            if cmd in f.get("keys"):
                result.append(f)
        return result

    # ### assistance ### #
    def __response(self, chat_id, res):
        if res:
            for i in res:
                if i:
                    self.bot.sendMessage(chat_id, i)

    def __split_msg(self, msg):
        ent = msg.get('entities', None)
        command = []
        offset = 0
        if ent:
            tmp = []
            for e in ent:
                if e['type'] == 'bot_command':
                    tmp.append(e)
                elif e['type'] == 'text_mention':
                    l = e['length']
                    o = e['offset']
                    offset -= l
                    repl = "@" + str(e['user']['id'])
                    offset += len(repl)
                    msg['text'] = msg['text'].replace(msg['text'][o:l + o], repl)

            if tmp:
                l0 = tmp[0]['length'] + offset
                o0 = tmp[0]['offset'] + offset
                for i in range(1, len(tmp)):
                    l1 = tmp[i]['length'] + offset
                    o1 = tmp[i]['offset'] + offset
                    command.append([
                        msg['text'][o0 + 1:o0 + l0],  # cmd
                        msg['text'][o0 + l0:o1].strip()
                    ])
                    o0 = o1
                    l0 = l1
                command.append([
                    msg['text'][o0 + 1: o0 + l0],  # cmd
                    msg['text'][o0 + l0:].strip()
                ])
                return command
            else:
                return None
        else:
            return None

    # ### NOT IMPLEMENTED ### #
    def new_participant(self, msg, chat_id):
        # TODO new_participant(not implemented)
        return None
        id = msg['new_chat_participant']['id']
        if not self.user.get_user_by_id(id):
            self.bot.sendMessage(chat_id, TEXT['new_user'] % str(id))


        tmp = msg['text'][1:].split(" ", 1)
        order = tmp[0].lower()
        if tmp.__len__() > 1:
            value = tmp[1]
        else:
            value = ""

        chat_id = str(chat_id)
        user_id = str(msg['from']['id'])
        user = money.user_get_by_uid(user_id)
        if user is not None:
            permission = int(user['permission'])
        else:
            return 0

        if order == "help" and permission >= 1:
            text = ""
            for i in money.function:
                text += i[2] + "\t\t" + i[3] + "\t\r\n"
            bot.sendMessage(chat_id, text, parse_mode="html")
            return 0

        for k in range(0, money.function.__len__()):
            if money.function[k][1] == order:
                if permission >= money.function[k][4]:
                    ret = money.function[k][0](money, value, user_id)
                    bot.sendMessage(chat_id, ret, parse_mode="html")
                else:
                    if debug:
                        print(user_id, money.function[k][0])
                break
        if chat.keyboard[1] == order:
            if permission >= chat.keyboard[4]:
                ret = chat.keyboard[0](chat, chat_id, user_id, value)
                bot.sendMessage(chat_id, ret[0], parse_mode="html")
                bot.sendMessage(chat_id, ret[1], reply_markup=ret[2], parse_mode="html")
            else:
                if debug:
                    print(user_id, money.function[k][0])
            return 0
        for k in range(0, chat.function.__len__()):
            if chat.function[k][1] == order:
                if permission >= chat.function[k][4]:
                    ret = chat.function[k][0](chat, chat_id, user_id, value)
                    bot.sendMessage(chat_id, ret, parse_mode="html")
                else:
                    if debug:
                        print(user_id, money.function[k][0])
                break
        return 0
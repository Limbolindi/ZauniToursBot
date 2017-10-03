
    def bot_add_uname(self, data_replay, data_replayed):
        # TODO ?? usage / funct
        data = []
        data.append(['i', data_replayed['from']['id']])
        data.append(['u', data_replayed['from'].get('username', None)])
        data.append(['n', data_replay['text'][1][1]])
        return self.bot_add_user(data)



    def get_user_by_id(self, id):
        """
        get a <user> object by the nickname
        wrapper-methode for _get(header,data)
        :param id: str(id) or int(id)
        :return: <user>
        """
        return self._get("id", id)

    def get_user_by_uname(self, uname):
        """
        get a <user> object by the nickname
        wrapper-methode for _get(header,data)
        :param uname: str(username)
        :return: <user>
        """
        return self._get("uname_lower", str(uname).lower())

    def get(self, data):
        """
        get a list of <users> from a string like "nick @id   @uname    nick    "
        :param data: array [[ -- , string with @id/@uname/nick]]
        :return: list of <user> elements and strings (Strings -> not found users)
        """
        data = data[0][1]
        ret = []
        data = str(data).strip().split(" ")[:]

        for i in range(0, len(data)):
            data[i] = data[i].strip()
        for d in data:
            if d:
                tmp = None
                if d[0] == "@":
                    if d[1:].isdigit():
                        tmp = self._get("id", int(d[1:]))
                    else:
                        tmp = self._get("uname_lower", str(d[1:]).lower())
                elif len(d) == 9:
                    if d[4:5] == ".":
                        tmp = self._get("nick_lower", str(d).lower())
                else:
                    tmp = None
                if tmp is not None:
                    tmp.pop(u'_id')
                    ret.append(tmp)
                else:
                    ret.append(d)
        return ret


    def add_user(self, nick, id=None, uname=None, security=0):




            # if the user exists -> and all data is set -> return
            if user.get('id', None) and user.get('uname', None):
                return TEXT['user_add'] % nick
            # if user exists -> and id is set
            if user.get('id', None):
                id = user.get('id',None)
            # if user exists -> and uname is set
            if user.get('uname', None):
                uname = user.get('uname', None)
            security = user.get('security', 0)



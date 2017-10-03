#!/usr/bin/env python
# -*- coding: utf-8-*-

from unittest import TestCase
from pymongo import MongoClient
from main.modules.users import UsersClass
import random
from main.tests.data import users, insert
MONGO= ["127.0.0.1", 27017, "tests", "users"]


class TestUser(TestCase):

    def __init__(self, *args, **kwargs):
        super(TestUser, self).__init__(*args, **kwargs)
        self.db = MongoClient(MONGO[0], MONGO[1])[MONGO[2]][MONGO[3]]
        self.user = UsersClass(self.db)

    def setUp(self):
        self.db.drop()
        for i in users:
            self.db.insert_one(i)
            i.pop('_id')
        self.assertEqual(self.db.count(), len(users))
        return 0

    def test_get_user_by_nick(self):
        for i in users:
            answer = self.user.get_user_by_nick(i["nick"])
            answer.pop("_id")
            self.assertEquals(answer, i)

            answer = self.user.get_user_by_nick(i["nick_lower"])
            answer.pop("_id")
            self.assertEquals(answer, i)

    def test_get_user_by_id(self):
        for i in users:
            answer = self.user.get_user_by_id(i["id"])
            answer.pop("_id")
            self.assertEquals(answer, i)

    def test_get_user_by_uname(self):
        for i in users:
            answer = self.user.get_user_by_uname(i["uname"])
            answer.pop("_id")
            self.assertEquals(answer, i)

            answer = self.user.get_user_by_uname(i["uname_lower"])
            answer.pop("_id")
            self.assertEquals(answer, i)

    #get

    def test_get__single(self):
        for i in users:
            answer = self.user.get(i["nick"])
            self.assertTrue(answer)
            self.assertEquals(answer[0], i)

            answer = self.user.get(i["nick_lower"])
            self.assertTrue(answer)
            self.assertEquals(answer[0], i)

            answer = self.user.get("@" + i["uname"])
            self.assertTrue(answer)
            self.assertEquals(answer[0], i)

            answer = self.user.get("@" + i["uname_lower"])
            self.assertTrue(answer)
            self.assertEquals(answer[0], i)

            answer = self.user.get("@" + str(i["id"]))
            self.assertTrue(answer)
            self.assertEquals(answer[0], i)

    def test_get__all_same(self):
        uname = "  "
        uname_lower = "  "
        nick = " "
        nick_lower = "  "
        id = "  "
        for i in users:
            uname += "@"+ i["uname"] + " "
            uname_lower += "@" + i["uname_lower"] + " "
            nick += i["nick"] + " "
            nick_lower += i["nick_lower"] + " "
            id += "@" + str(i["id"]) + " "

        self.assertEqual(self.user.get(uname), users)
        self.assertEqual(self.user.get(uname_lower), users)
        self.assertEqual(self.user.get(nick), users)
        self.assertEqual(self.user.get(nick_lower), users)
        self.assertEqual(self.user.get(id), users)

    def test_get__all_random(self):
        for i in users:
            tmp = []
            tmp.append("@"+ i["uname"])
            tmp.append("@" + i["uname_lower"])
            tmp.append(i["nick"])
            tmp.append(i["nick_lower"])
            tmp.append("@" + str(i["id"]))
            self.assertEqual(self.user.get(" ".join(tmp)), [i,i,i,i,i])

        tmp2 = []
        for i in users:
            tmp = []
            tmp.append("@"+ i["uname"])
            tmp.append("@" + i["uname_lower"])
            tmp.append(i["nick"])
            tmp.append(i["nick_lower"])
            tmp.append("@" + str(i["id"]))
            tmp2.append(tmp[random.randint(0,4)])
        self.assertEqual(self.user.get(" ".join(tmp2)), users)

        tmp2 = []
        for i in users:
            tmp = []
            tmp.append("@" + i["uname"])
            tmp.append("@" + i["uname_lower"])
            tmp.append(i["nick"])
            tmp.append(i["nick_lower"])
            tmp.append("@" + str(i["id"]))
            tmp2.append(tmp[random.randint(0, 4)])
        self.assertEqual(self.user.get(" ".join(tmp2)), users)

    def test_get__wrong(self):
        x = "aaaaaaaaa"
        self.assertEqual(self.user.get(x)[0], x)
        x = "@aaaaaaaaa"
        self.assertEqual(self.user.get(x)[0], x)
        x = "@1123aaaaaa"
        self.assertEqual(self.user.get(x)[0], x)
        x = "@99999999"
        self.assertEqual(self.user.get(x)[0], x)
        x = "oooo.oooo"
        self.assertEqual(self.user.get(x)[0], x)
        x = "<ase.asde"
        self.assertEqual(self.user.get(x)[0], x)
        x = ");.adassa"
        self.assertEqual(self.user.get(x)[0], x)
        x = ""
        self.assertFalse(self.user.get(x))
        x = " "
        self.assertFalse(self.user.get(x))
        x = "   "
        self.assertFalse(self.user.get(x))
        x = "\t"
        self.assertFalse(self.user.get(x))
        x = "\n"
        self.assertFalse(self.user.get(x))

    def test_get__special(self):
        special = "\n\t\r"
        for x in special:
            for i in users:
                tmp = []
                tmp.append(x + "@"+ i["uname"])
                tmp.append(x + "@" + i["uname_lower"])
                tmp.append(x + i["nick"])
                tmp.append(x + i["nick_lower"])
                tmp.append(x + "@" + str(i["id"]))
                self.assertEqual(self.user.get(" ".join(tmp)), [i,i,i,i,i])
        for x in special:
            for i in users:
                tmp = []
                tmp.append("@"+ i["uname"] + x )
                tmp.append("@" + i["uname_lower"] + x )
                tmp.append(i["nick"] + x )
                tmp.append(i["nick_lower"] + x )
                tmp.append("@" + str(i["id"]) + x )
                self.assertEqual(self.user.get(" ".join(tmp)), [i,i,i,i,i])

    #add_user

    def test_add_user__full(self):
        for i in insert:
            ret = self.user.add_user(nick=i['nick'], id=i['id'], uname=i['uname'])
            self.assertEqual(ret, 0)

        self.assertEqual(self.db.count(), len(users) + len(insert))

        request = []
        for i in insert:
            tmp = []
            tmp.append("@" + i["uname"])
            tmp.append("@" + i["uname_lower"])
            tmp.append(i["nick"])
            tmp.append(i["nick_lower"])
            tmp.append("@" + str(i["id"]))
            request.append(tmp[random.randint(0, 4)])
        self.assertEqual(self.user.get(" ".join(request)), insert)

    def test_add_user__minimal(self):
        answer = []
        for i in insert:
            ret = self.user.add_user(nick=i['nick'])
            self.assertEqual(ret, 0)
            answer.append(i.copy())
        for i in answer:
            i.pop('uname')
            i.pop('uname_lower')
            i.pop('id')
        self.assertEqual(self.db.count(), len(users) + len(insert))

        request = []
        for i in insert:
            tmp = []
            tmp.append(i["nick"])
            tmp.append(i["nick_lower"])
            request.append(tmp[random.randint(0, 1)])
        self.assertEqual(self.user.get(" ".join(request)), answer)

    def test_add_user__id(self):
        answer = []
        for i in insert:
            ret = self.user.add_user(nick=i['nick'], id=i['id'])
            self.assertEqual(ret, 0)
            answer.append(i.copy())
        for i in answer:
            i.pop('uname')
            i.pop('uname_lower')

        self.assertEqual(self.db.count(), len(users) + len(insert))

        request = []
        for i in insert:
            tmp = []
            tmp.append(i["nick"])
            tmp.append(i["nick_lower"])
            tmp.append("@" + str(i["id"]))
            request.append(tmp[random.randint(0, 2)])

        self.assertEqual(self.user.get(" ".join(request)), answer)

    def test_add_user__uname(self):
        answer = []
        for i in insert:
            ret = self.user.add_user(nick=i['nick'], uname=i['uname'])
            self.assertEqual(ret, 0)
            answer.append(i.copy())
        for i in answer:
            i.pop('id')

        self.assertEqual(self.db.count(), len(users) + len(insert))

        request = []
        for i in insert:
            tmp = []
            tmp.append("@" + i["uname"])
            tmp.append("@" + i["uname_lower"])
            tmp.append(i["nick"])
            tmp.append(i["nick_lower"])
            request.append(tmp[random.randint(0, 3)])
        self.assertEqual(self.user.get(" ".join(request)), answer)

    def test_add_user__double(self):
        from main.static import users as TXT
        for i in users:
            ret = self.user.add_user(nick=i['nick'], id=i['id'], uname=i['uname'])
            self.assertEqual(ret, TXT['user_add'] % i['nick'])
        self.assertEqual(self.db.count(), len(users))

        for i in users:
            ret = self.user.add_user(nick=i['nick'], uname=i['uname'])
            self.assertEqual(ret, TXT['user_add'] % i['nick'])
        self.assertEqual(self.db.count(), len(users))

        for i in users:
            ret = self.user.add_user(nick=i['nick'], id=i['id'])
            self.assertEqual(ret, TXT['user_add'] % i['nick'])
        self.assertEqual(self.db.count(), len(users))
        for i in users:
            ret = self.user.add_user(nick=i['nick'])
            self.assertEqual(ret, TXT['user_add'] % i['nick'])
        self.assertEqual(self.db.count(), len(users))

    def test_add_user__update(self):
        #update minimal -> full
        self.test_add_user__minimal()
        for i in insert:
            ret = self.user.add_user(nick=i['nick'], id=i['id'], uname=i['uname'])
            self.assertEqual(ret, 0)
            ret = self.user.get_user_by_nick(i['nick'])
            ret.pop('_id')
            self.assertEqual(ret,i)
        self.assertEqual(self.db.count(), len(users) + len(insert))

        # update uname -> full
        self.setUp()
        self.assertEqual(self.db.count(), len(users))
        self.test_add_user__uname()
        for i in insert:
            ret = self.user.add_user(nick=i['nick'], id=i['id'], uname=i['uname'])
            self.assertEqual(ret, 0)
            ret = self.user.get_user_by_nick(i['nick'])
            ret.pop('_id')
            self.assertEqual(ret, i)
        self.assertEqual(self.db.count(), len(users) + len(insert))

        # update id -> full
        self.setUp()
        self.assertEqual(self.db.count(), len(users))
        self.test_add_user__id()
        for i in insert:
            ret = self.user.add_user(nick=i['nick'], id=i['id'], uname=i['uname'])
            self.assertEqual(ret, 0)
            ret = self.user.get_user_by_nick(i['nick'])
            ret.pop('_id')
            self.assertEqual(ret,i)
        self.assertEqual(self.db.count(), len(users) + len(insert))

        # update minimal -> uname
        self.setUp()
        self.assertEqual(self.db.count(), len(users))
        self.test_add_user__minimal()
        for i in insert:
            ret = self.user.add_user(nick=i['nick'], uname=i['uname'])
            self.assertEqual(ret, 0)
            ret = self.user.get_user_by_nick(i['nick'])
            ret.pop('_id')
            x = i.copy()
            x.pop('id')
            self.assertEqual(ret, x)
        self.assertEqual(self.db.count(), len(users) + len(insert))

        #update minimal -> id
        self.setUp()
        self.assertEqual(self.db.count(), len(users))
        self.test_add_user__minimal()
        for i in insert:
            ret = self.user.add_user(nick=i['nick'], id=i['id'])
            self.assertEqual(ret, 0)
            ret = self.user.get_user_by_nick(i['nick'])
            ret.pop('_id')
            x = i.copy()
            x.pop('uname')
            x.pop('uname_lower')
            self.assertEqual(ret, x)
        self.assertEqual(self.db.count(), len(users) + len(insert))

        # don't update anything
        self.setUp()
        self.assertEqual(self.db.count(), len(users))
        self.test_add_user__minimal()
        for i in insert:
            ret = self.user.add_user(nick=i['nick'])
            self.assertEqual(ret, 0)
            ret = self.user.get_user_by_nick(i['nick'])
            ret.pop('_id')
            x = i.copy()
            x.pop('id')
            x.pop('uname')
            x.pop('uname_lower')
            self.assertEqual(ret, x)
        self.assertEqual(self.db.count(), len(users) + len(insert))

        # update uname -> uname
        self.setUp()
        self.assertEqual(self.db.count(), len(users))
        self.test_add_user__uname()
        for i in insert:
            ret = self.user.add_user(nick=i['nick'], uname=i['uname'])
            self.assertEqual(ret, 0)
            ret = self.user.get_user_by_nick(i['nick'])
            ret.pop('_id')
            x = i.copy()
            x.pop('id')
            self.assertEqual(ret, x)
        self.assertEqual(self.db.count(), len(users) + len(insert))

        # update id -> id
        self.setUp()
        self.assertEqual(self.db.count(), len(users))
        self.test_add_user__id()
        for i in insert:
            ret = self.user.add_user(nick=i['nick'], id=i['id'])
            self.assertEqual(ret, 0)
            ret = self.user.get_user_by_nick(i['nick'])
            ret.pop('_id')
            x = i.copy()
            x.pop('uname')
            x.pop('uname_lower')
            self.assertEqual(ret, x)
        self.assertEqual(self.db.count(), len(users) + len(insert))

    def test_add_user__wrong(self):
        from main.static import users as TXT
        invalid_names = [
            "Maximilian", # to long
            "Lindpointner", # to long
            "LimboLindi", # to long
            "1111.111", # to short
            "aaaaa.aaa", # invalid format
            "&asd.asdf", # string.punctation
            "asdfQasdf", # missing .
            "asdf!asdf", # missing .
            "asdfasdf", # to short/missing .
            "", # empty
            None # error?
        ]
        for i in invalid_names:
            ret = self.user.add_user(nick=i)
            self.assertEqual(ret, TXT['invalid_nick'] % i)




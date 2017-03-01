#!/usr/bin/env python
# -*- coding: utf-8-*-

import time
#from pymongo import MongoClient
import pymongo
from decimal import Decimal
import json
import data
from money import Struckt
from data import MSG, CAR

class Chat(Struckt):

    def block(self, chat_id, seat, comment, carNR=1):
        pass
    def check_seat(self, chat_id, seat, carNR=1):
        car = self.get_car(chat_id, carNR)
        for key in car.keys():
            if key == seat:
                if car[key] == "0000":
                    return 0
                    pass
                else:
                    return 1
                    pass
        return MSG['car_wrong_seat'] % seat

    def add_car(self):
        pass


    function = [
        ["funktion", "comman", "usage", "help", 0],
        [set_chat,      "set",      "/set",         "starts Car-Bot",           8],
        [set_seat,      "seat",     "/seat",        "reserves a seat",          4],
        [show,          "showcar",  "/showcar",     "shows cars",               4],
        [free,          "free",     "/free",        "",                         8],
        [block,         "block",    "/block",       "",                         8],

    ]
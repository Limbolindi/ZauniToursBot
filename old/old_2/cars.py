#!/usr/bin/env python
# -*- coding: utf-8-*-

import time
#from pymongo import MongoClient
import pymongo
from decimal import Decimal
import json
import data
from data import MSG, CAR, Struckt

class Cars:

    def __init__(self, database_users, database_cars):
        self.cars = self.__Cars(database_users, database_cars)

    class __Cars(Struckt):

        def __init__(self, database_users, database_cars):

            super(self.__class__, self).__init__(database_users)

            if type(database_cars) is not pymongo.collection.Collection:
                raise TypeError(type(database_cars))
            self.cars = database_cars







"""












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

"""
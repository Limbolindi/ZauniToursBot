#!/usr/bin/env python
# -*- coding: utf-8-*-

import time
#from pymongo import MongoClient
import pymongo
from decimal import Decimal
import json
import data
from user import Struckt
from data import MSG, CAR

class Chat(Struckt):
    chats = None
    def __init__(self, mongodb, mongo_chats):
        """
        :type mongodb: pymongo.collection.Collection
        """
        if type(mongodb) is not pymongo.collection.Collection:
            raise TypeError(type(mongodb))
        self.mongodb = mongodb

        if type(mongo_chats) is not pymongo.collection.Collection:
            raise TypeError(type(mongo_chats))
        self.chats = mongo_chats

    def get_chat(self, chat_id):
        return self.chats.find_one({"chat_id": chat_id})

    def set_chat(self, chat_id, cars=1):
        result = self.get_chat(chat_id)
        if result is not None:
            return MSG['chat_already_exists']
        data = []
        car = {
            "A1": "0000",
            "A3": "0000",
            "B1": "0000",
            "B2": "0000",
            "B3": "0000"
        }
        for i in range(0,cars):
            data.append(car)
        result = self.chats.update_one({"chat_id": chat_id}, {"$set": {"cars": data}}, upsert=True)
        if result.raw_result["ok"] is not 1 or result.acknowledged is False:
            return MSG['error_mongo_setchat'] % chat_id
        else:
            return MSG['chat_created'] % chat_id

    def show(self, chat_id, car=1):
        result = self.get_chat(chat_id)
        if result is None:
            return MSG['unknown_chat'] % chat_id
        cars = result.get("cars",[])
        if cars.__len__() < car:
            return MSG['car_not_found'] % (chat_id, car)

        text = self.get_car(cars[car])
        text += "\n\n"
        for k in cars[car].keys():
            if cars[car][k] is not "0000":
                text += str(k) + ": " + self.user_get_by_uid(cars[car][k])


    def get_car(self, car):
        A1 = CAR['check'] if car.get("A1", "0000")  == "0000" else CAR['cross']
        A3 = CAR['check'] if car.get("A3", "0000")  == "0000" else CAR['cross']
        B1 = CAR['check'] if car.get("B1", "0000")  == "0000" else CAR['cross']
        B2 = CAR['check'] if car.get("B2", "0000")  == "0000" else CAR['cross']
        B3 = CAR['check'] if car.get("B3", "0000")  == "0000" else CAR['cross']
        data = CAR['head'] + CAR['wall'] + CAR['A'] % (A1, A3) + CAR['space', + CAR['B'] % (B1, B2, B3) + CAR['space'] + CAR['back'] + CAR['wall']
    def set_seat(self, chat_id, seat, car=1):
        pass
    def free(self, chat_id, seat, car=1):
        pass
    def block(self, chat_id, seat, comment, car=1):
        pass
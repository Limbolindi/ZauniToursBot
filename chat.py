#!/usr/bin/env python
# -*- coding: utf-8-*-

from data import MSG, Struckt, CAR
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import pymongo


#, zauni="10942671"

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

    def get_cars(self, chat_id):
        result = self.get_chat(chat_id)
        if result is None:
            return None
        cars = result.get("cars", [])
        return cars

    def print_car(self, car, driver='ghost'):
        A1 = CAR['check'] if car.get("A1", "0000")  == "0000" else CAR['cross']
        A3 = CAR['check'] if car.get("A3", "0000")  == "0000" else CAR['cross']
        B1 = CAR['check'] if car.get("B1", "0000")  == "0000" else CAR['cross']
        B2 = CAR['check'] if car.get("B2", "0000")  == "0000" else CAR['cross']
        B3 = CAR['check'] if car.get("B3", "0000")  == "0000" else CAR['cross']
        data = CAR['head'] + CAR['wall'] + CAR['A'] % (CAR[driver], A3) + CAR['space'] + CAR['B'] % (B1, B2, B3) + CAR['space'] + CAR['back'] + CAR['wall']
        return data

    def get_free(self, chat_id):
        cars = self.get_cars(chat_id)
        result = []
        for i in range(0, cars.__len__()):
            for seat in cars[i].keys():
                if cars[i][seat] == "0000":
                    result.append([i, seat])
        return result



    def update_seat(self, chat_id, car_id, seat, value):
        result = self.chats.update_one({"chat_id": chat_id}, {
            "$set": {"cars." + str(car_id) + "." + seat: value}
        })
        # TODO check result
        # TODO return?

    def get_seats_keyboard(self, chat_id):
        result = self.get_free(chat_id)
        keys = []
        for i in result:
            keys.append([InlineKeyboardButton(
                text="car %s, Seat: %s" % (i[0], i[1]), callback_data="%s;%s;%s" % (chat_id, i[0], i[1]))]
            )

        return [self.show(chat_id), MSG['select_seat'],InlineKeyboardMarkup(inline_keyboard=keys, one_time_keyboard=True)]

    def free(self, chat_id, car_id, seat):
        cars = self.get_cars(chat_id)
        if car_id < cars.__len__():
            if seat in cars[0].keys():
                return self.update_seat(chat_id, car_id, seat, "0000")
            else:
                #TODO unknown seat
                pass
        else:
            #TODO unknown car
            pass

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

    def show(self, chat_id):
        text = u""
        cars = self.get_cars(chat_id)
        if cars is None:
            return MSG['unknown_chat'] % chat_id
        for car in cars:
            text += self.print_car(car)
            text += "\n\n"
            for seat in car.keys():
                if car[seat] != "0000":
                    user = self.user_get_by_uid(car[seat])
                    if user is None:
                        text += str(seat) + ": " + car[seat] + "\n"
                    else:
                        text += str(seat) + ": " + user.get("name","user") + "\n"
        return text

    def free_seat(self, chat_id, user_id):
        cars = self.get_cars(chat_id)
        for i in range(0, cars.__len__()):
            for seat in cars[i].keys():
                if seat == user_id:
                    # TODO ??
                    return self.update_seat(chat_id, i, seat, "0000")
        # TODO msg missing user_id!
        return 0

    def set_seat(self, chat_id, car, seat, user_id):
        result = self.update_seat(chat_id, car, seat, user_id)
        return result



    def W_get_seats_keyboard(self, chat_id, user_id, data):
        return self.get_seats_keyboard(chat_id)

    def W_set_chat(self, chat_id, user_id, data):
        try:
            cars = int(data)
        except:
            cars = 1
        return self.set_chat(chat_id, cars)

    def W_show(self, chat_id, user_id, data):
        return self.show(chat_id)

    def W_free_seat(self, chat_id, user_id, data):
        return self.free_seat(chat_id, user_id)

    function = [
        [W_set_chat, "setcar", "/setcar", "", 8],
        [W_show, "showcar", "/showcar", "", 4],
        [W_free_seat, "free", "/free", "", 4]
    ]
    keyboard = [W_get_seats_keyboard, "seat", "/seat", "", 4]















#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pymongo import MongoClient
import time
import json
import hashlib
MONGO = MongoClient("127.0.0.1",27017)["zaunitours"]
money = {
        "time": str(time.strftime("%Y-%m-%d---%H:%M:%S")),
        "text": "start",
        "value": 0,
        "by": "000000"
    }
id = hashlib.sha256(json.dumps(money)).hexdigest()[:16]
result = MONGO.zt_users.update_one({"id": id}, {"$set": {"permission": 0, "nick": "Lindi", "value": 0, "money": [money]}}, upsert=True)
print result.acknowledged


exit(0)

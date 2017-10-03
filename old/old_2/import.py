#!/usr/bin/env python
# -*- coding: utf-8-*-
import argparse

from main import main

if __name__ == "__main__":
    #TODO description
    parser = argparse.ArgumentParser(description='description')
    required = parser.add_argument_group("required arguments")
    required.add_argument('conf', help='configfile', type=file)
    parser.add_argument("-n", metavar="NAMES", dest="namefile", type=file, help='names list\n')
    parser.add_argument("-v", metavar="VALUES", dest="valuefile", type=file, help='value list\n')
    parser.add_argument("-u", metavar="USERS", dest="userfile", type=file, help='user list\n')
    args = parser.parse_args()
    main.__init__(args.conf)

    try:
        if args.namefile is not None:
            data = list(args.namefile.readlines())
            for i in range(0, data.__len__()-1):
                if data[i][0] is "#":
                    data.pop(i)
            for i in data:
                print main.money.add_user(str(i).replace("\n", ""), user_id="000000")

        if args.valuefile is not None:
            data = list(args.valuefile.readlines())
            for i in data:
                tmp = i.replace("\n","").replace("€","").split(";")
                print main.money.add("[i] übertrag aus Liste;" + tmp[0] + ";" + tmp[1], "000000")

        if args.userfile is not None:
            data = list(args.userfile.readlines())
            for i in range(0, data.__len__()-1):
                if data[i][0] is "#":
                    data.pop(i)
            for i in data:
                tmp = i.replace("\r","").replace("\n","").split(";")
                if tmp.__len__() < 4:
                    print "Too less Arguments: %s" % i
                    break
                nick = str(tmp[0]).lower()
                user_id = str(tmp[1])
                permission = int(tmp[2])
                name = str(tmp[3])
                result =  main.money.mongodb.update_one(
                    {"nick_lower": nick.lower()},
                    {"$set": {
                        "permission": permission,
                        "name": name,
                        "user_id": user_id
                    }})
                print "%s{acknowledged: %s, matched: %s, modified: %s}\n" % \
                      (i, result.acknowledged, result.matched_count, result.modified_count)
    except:
        import traceback
        traceback.print_exc()
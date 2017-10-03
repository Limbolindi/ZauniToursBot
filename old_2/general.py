#!/usr/bin/env python
# -*- coding: utf-8-*-

import json










def debug_f(msg):
    # TODO shiti
    __debug_exit = False
    # print whole telegram msg as json dump
    __debug_print = True
    # print plain msg
    __debug_printcpy = False
    # testcase
    __debug_test = False
    ##
    if not debug:
        return
    if __debug_print:
        print(json.dumps(msg, indent=4))
    if __debug_printcpy:
        print(msg)
    if __debug_test:
        pass
    if __debug_exit:
        pass
    return
# -*- coding: utf-8 -*-
from case.test_json.dialogtest import runcase
from case.test_json.pubshjson import generatejson_push
""""
自由发挥
"""
def run():
    randphone = False
    case="waihu_chongqing"
    runcase(case,randphone,3)
if __name__=='__main__':
    run()
    # pushjson()
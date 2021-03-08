# -*- coding: utf-8 -*-
from case.test_json.dialogtest import runcase
from case.test_json.getjson import SynJson
from case.test_json.pubshjson import generatejson_push

""""
自由发挥
"""


# randphone = True
def sffengchao():
    case = "sffengchao"
    runcase(case)

def wh_fengchao():
    case = "wh_fengchao"
    runcase(case)


def pushjson():
    botname = "丰巢_无法取件"
    env = "beta"
    modfiy = {

        "operationFunctions": [{"name": "node-b3dd6e91-0cac-4a94-80cd-44e63236a024",
                                "uri": "http://10.32.2.209:8091/inter/api/v1/fengchao/queryCustomerInfo"}],
    }
    generatejson_push(botname, env, modfiy)


def fengchaocallin():
    case = "fengchaocallin"
    runcase(case)


if __name__ == '__main__':
    # sffengchao()
    # wh_fengchao()
    # wh_fengchao()
    # wh_fengchao()
    # wh_fengchao()
    pushjson()
    # fengchaocallin()
# -*- coding: utf-8 -*-
from case.test_json.dialogtest import runcase
from case.test_json.pubshjson import generatejson_push
from case.test_json.getjson import SynJson
""""
自由发挥
"""
def run():
    case="yanchengnongshanghang"
    case="anjiewaihu_yancheng"
    runcase(case)

def betapushjson():
    botname = "盐城消费贷催收外呼"
    botname="盐城农商行按揭贷款催收"
    synjson = SynJson(botname)
    synjson.getjson()
    modfiy = {
        "operationFunctions": [{
            "name": "getOutboundParams",
            "uri": "http://10.32.2.209:8091/slots/api/v1/getSlots",
            # "valueType": "str",
            # "initValue": "http://10.12.6.75:8091/ics-web/ICSRequest.action"
        }]
    }
    # modfiy=None
    # file = r"c:/speech/德邦/DepponExpress_1581312291884.json"
    # file=r"C:/Users/aispeech/Downloads/DepponExpress_1585190729781.json"
    env = "beta"
    generatejson_push(botname, env,modfiy)

if __name__=='__main__':
    run()
    # betapushjson()
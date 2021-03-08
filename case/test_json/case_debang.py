# -*- coding: utf-8 -*-
from case.test_json.dialogtest import runcase
from case.test_json.pubshjson import generatejson_push
from case.test_json.getjson import SynJson
import requests

""""
自由发挥
"""


class CourierTime:
    WEE_HOUR = 1
    OFFICE_HOUR = 2
    CLOSING_TIME = 3


class DepponCustomTime:
    CUSTOM_TIME = 1
    NO_CUSTOM_TIME = 0


def update_time_inpart(value):
    url = "http://47.98.151.178:8091/inter/api/v1/deppon/updateTimeInPart"
    body = {"dataFlag": value}
    print("update_time_inpart req: ", body)
    re = requests.post(url=url, json=body)
    print("update_time_inpart resp: ", re.text)


def update_customtime(value):
    url = "http://47.98.151.178:8091/inter/api/v1/deppon/updateCustomTime"
    body = {"inCustom": value}
    print("update_customtime req: ", body)
    re = requests.post(url=url, json=body)
    print("update_customtime resp: ", re.text)


def run():
    betapushjson()
    randphone = False
    case = "debangba_test.xlsx"
    # case = "debangba_test_yaundan.xlsx"

    update_customtime(DepponCustomTime.CUSTOM_TIME)  # 置为人工客服时间
    update_time_inpart(CourierTime.OFFICE_HOUR)  # 置为快递员上班时间
    sheetnames = ["查件", "咨询网点", "下单", "ivr", "价格咨询", "查件alpha", "查询网点alpha", "禁止下单地址"]
    runcase(case, randphone, sheetnames=sheetnames, threadnum=15)


    update_time_inpart(CourierTime.CLOSING_TIME)  # 置为快递员下班时间
    sheetnames = ["下班时间下单", "下班时间ivr", ]
    runcase(case, randphone, sheetnames=sheetnames, threadnum=15)
    sheetnames = ["重复来电新", ]
    runcase(case, randphone, sheetnames=sheetnames, threadnum=1)


    update_customtime(DepponCustomTime.NO_CUSTOM_TIME)  # 置为非人工客服时间
    update_time_inpart(CourierTime.OFFICE_HOUR)  # 置为快递员上班时间
    sheetnames = ["非人工时间测试"]
    runcase(case, randphone, sheetnames=sheetnames, threadnum=15)
def pushjson():
    botname = "DepponExpress"
    modfiy = {
        "botVariables": [{
            "variableName": "deppon_uri",
            "valueType": "str",
            "initValue": "http://10.12.6.75:8091/ics-web/ICSRequest.action"
        },
            {
                "variableName": "deppon_write_uri",
                "valueType": "str",
                "initValue": "http://10.12.6.75:8091/ics-web/ICSRequestAction.action",
                "variableDescription": "德邦测试：http://27.115.3.108:10318/ics-web/ICSRequestAction.action     德邦线上：http://180.153.24.170/ics-web/ICSRequest.action"
            }
        ]
    }
    env = "test"
    generatejson_push(botname, env, modfiy)


def betapushjson(**kwargs):
    botname = "DepponExpress"
    modfiy = {
        "botVariables": [
            {
                "variableName": "deppon_uri",
                "valueType": "str",
                "initValue": "http://10.32.2.209:8091/ics-web/ICSRequest.action"
            },
            {
                "variableName": "deppon_write_uri",
                "valueType": "str",
                "initValue": "http://10.32.2.209:8091/ics-web/ICSRequestAction.action",
                "variableDescription": "德邦测试：http://27.115.3.108:10318/ics-web/ICSRequestAction.action     德邦线上：http://180.153.24.170/ics-web/ICSRequest.action"
            }
        ],
        "operationFunctions": [{"name": "node-63619712-2c6c-4ca0-bebb-c9427fd5c7e1",
                                "uri": "http://10.32.2.209:8091/inter/api/v1/deppon/queryOrderByPhone"
                                },
                               {"name": "node-67d8e213-f992-4e35-8fcc-6a570dbd3d48",
                                "uri": "http://10.32.2.209:8091/inter/api/v1/deppon/queryOrderByPhone"
                                },
                               {"name": "queryTimeInWork",
                                "uri": "http://10.32.2.209:8091/inter/api/v1/deppon/queryTimeInPart"
                                },
                               {"name": "node-4297f75d-c20f-4939-aeeb-c67e68b04681",
                                "uri": "http://10.32.2.209:8091/inter/api/v1/deppon/queryCustomTime"
                                }
                               ]
    }
    env = "beta"
    generatejson_push(botname, env, modfiy, importintent="v1",**kwargs)


def pushorder():
    botname = "快递下单地址收集v2"
    modfiy = None
    env = "test"
    generatejson_push(botname, env, modfiy)


def run_test():
    randphone = False
    case = "debangba_test.xlsx"
    # case = "debangba_test_yaundan.xlsx"
    update_time_inpart(CourierTime.OFFICE_HOUR)  # 置为上班时间
    sheetnames = ["查件", "咨询网点", "下单", "ivr", "价格咨询", "查件alpha", "查询网点alpha"]
    runcase(case, randphone, sheetnames=sheetnames, threadnum=20)


if __name__ == '__main__':
    run()
     # middle end  out
    # betapushjson()
    # betapushjson(debang_fesival="middle",debang_order=True)
    # betapushjson(debang_fesival="end")
    # betapushjson(debang_fesival="out")
    # betapushjson()
    # update_time_inpart(CourierTime.OFFICE_HOUR)
    # update_time_inpart(CourierTime.CLOSING_TIME)
    # update_customtime(DepponCustomTime.CUSTOM_TIME)
    # update_customtime(DepponCustomTime.NO_CUSTOM_TIME)
    # for i  in range(101):
    #     run_test()

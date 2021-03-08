# -*- coding: utf-8 -*-
from case.test_json.pubshjson import generatejson_push
from case.test_json.dialoguewithtxt import dialoguetxt


def run_txt():
    pass
    phone = '1028'
    pid = "914005519"
    mobilephone = '13580594404'
    env = 'alpha'
    file = "test"
    # file = "侵权单"
    # file = "正式报关"
    # file = "提供公司信息"
    callout5 = {
        "appId": 7,
        "waybillNo": "785915728240",
        "from": "香港",
        "to": "北京",
        "tax": 345.6000
    }
    callout16 = {
        "appId": 16,
        "waybillNo": "785915728240",
        "from": "香港",
        "to": "北京",
        "tax": "345.6000",
        "customerName": "关务测试"
    }
    callout = {
        "appId": 17,
        "waybillNo": "785915728240",
        "from": "香港",
        "to": "北京",
        "tax": 345.6000,
        "customerName": "关务测试"
    }
    callout18 = {
        "appId": 18,
        "waybillNo": "785915728240",
        "from": "香港",
        "to": "北京",
        "tax": "345.6000",
        "customerName": "关务测试",
        "declaredValuecny": "6666",
        "declaredValue": "8888",
        "valueUnit": "人民币"
    }
    callout19 = {
        "appId": 19,
        "waybillNo": "785915728240",
        "from": "香港",
        "to": "北京",
        "tax": 345.6000,
        "customerName": "关务测试"
    }
    callout20 = {
        "appId": 20,
        "waybillNo": "785915728240",
        "from": "香港",
        "to": "北京",
        "tax": "345.6000",
        "text_content": "123",
        "customerName": "关务测试"
    }
    checklabel = {"flowResult": "flowResult"}
    dialogue = dialoguetxt(env, phone, pid, file, calloutparam=callout5,checklabel=checklabel)
    dialogue.testcase()


if __name__ == '__main__':
    run_txt()
    # pushjson()

# -*- coding: utf-8 -*-
from case.test_json.dialoguewithtxt import dialoguetxt
import requests


def sendmsg():
    pid = "914009574"
    mobilephone = '13580594404'
    env = 'beta'
    file = "test"
    body = {"callId": "1851358396028ff5f923f6311eb852970c94ee2fee8", "allSilence": "0", "cityCode": "010",
            "isArtificial": 1, "callNum": "18513583960", "callNumOrigin": "18513583960", "intent": "0/3",
            "artificialNode": "主动转人工"}

    dialogue = dialoguetxt(env, mobilephone, pid, file)
    url = "http://s-gateway-beta.talkinggenie.com/inter/api/v1/sf/sendMsg"
    for i in range(1000):
        phone = dialogue.getphone()
        body["callNum"] = phone
        body["callNumOrigin"] = phone
        r = requests.post(url=url, json=body)
        print(r.text)


def run_txt():
    pass
    phone = '1028'
    pid = "914009574"
    # pid="914007918"
    mobilephone = '13580594404'
    # env = 'test'
    # env = 'alpha'
    env = 'beta'
    # env='prod'
    # file = "查单"
    file = "test"
    # file = "高峰期时效外"
    # file = "高峰期时效内"
    # file = "高峰期时效内会员关"
    # file = "ivr"
    # file="text_message"
    # file = "backlisthit"
    # file = "特殊查单"
    # file = "模糊查单"
    # file = "流程优化"
    # file="价格咨询"
    # file="下单"
    # file = "回拨流程"
    dialogue = dialoguetxt(env, phone, pid, file)
    # dialogue.url = "http://47.97.158.11:19103/dataclean/message/yto/messages/v2"
    dialogue.testcase()


if __name__ == '__main__':
    run_txt()
    # pushjson()
    # sendmsg()

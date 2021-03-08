# -*- coding: utf-8 -*-
from case.test_json.pubshjson import generatejson_push
from case.test_json.dialoguewithtxt import dialoguetxt


def run_txt():
    pass
    phone = '998'
    pid = "914006674"
    # pid="914007918"
    mobilephone = '13580594404'
    # env = 'test'
    # env = 'alpha'
    env = 'beta'
    # env='prod'
    # file = "查单"
    # file="价格咨询"
    # file = "正常时间流程"
    file = "test"
    # file = "ivr"
    # file = "deptmatch"
    # file = "下单"
    # file = "下班时间下单"
    # file="查询网点"
    pushdeppon = False
    randphone = False
    # randphone = True
    dialogue = dialoguetxt(env, phone, pid, file, randphone=randphone, pushdeppon=pushdeppon)
    dialogue.testcase()


if __name__ == '__main__':
    run_txt()
    # pushjson()

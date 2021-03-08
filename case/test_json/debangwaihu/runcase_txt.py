# -*- coding: utf-8 -*-
from case.test_json.pubshjson import generatejson_push
from case.test_json.dialoguewithtxt import dialoguetxt


def run_txt():
    pass
    phone = '1028'
    pid = "914012133"
    # pid="914007918"
    mobilephone = '13580594404'
    # env = 'test'
    env = 'alpha'
    # env = 'beta'
    # env='prod'
    file = "test"
    # file="拒绝"
    # file="接受已发拒绝"
    file="intent"
    # file="tests"
    pushdeppon = False
    randphone = False
    # randphone = True
    checklable = {"user_type": "用户等级"}
    dialogue = dialoguetxt(env, phone, pid, file, checklabel=checklable)
    dialogue.testcase()


if __name__ == '__main__':
    run_txt()
    # pushjson()

# -*- coding: utf-8 -*-
from case.test_json.dialoguewithtxt import dialoguetxt

"""
顺丰全场景 txt测试。
"""


def run():
    phone = '1026'
    pid = "914012099"
    # mobilephone = '13580594404'
    # env = 'test'
    env = 'alpha'
    # env = 'beta'
    # env = 'prod'
    # file = "查单"
    file = "test"
    # file = "testprod"
    # file="testbak"
    # file = "generatecase.txt"
    lables = {"is_benren": "是否接到疑似诈骗电话", "is_shouji": "能否提供诈骗手机号", "result_phone_num": "诈骗手机号",
              "is_other": "能否提供诈骗QQ或者微信", "is_qq": "能否提供诈骗QQ号", "result_num": "诈骗QQ号",
              "is_weixin": "能否提供诈骗微信号", "num_weixin": "诈骗微信号"}
    # lables = None
    dialogue = dialoguetxt(env, phone, pid, file, checklabel=lables)
    dialogue.testcase()


if __name__ == '__main__':
    run()
    # i = 0
    # while i < 5:
    #     i = i + 1
    #     run()

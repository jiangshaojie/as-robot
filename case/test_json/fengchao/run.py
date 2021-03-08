# -*- coding: utf-8 -*-
from case.test_json.dialoguewithtxt import dialoguetxt

"""
顺丰全场景 txt测试。
"""


def run():
    phone = '1026'
    pid = "914008741"
    # mobilephone = '13580594404'
    # env = 'test'
    # env = 'alpha'
    env = 'beta'
    file = "test"
    dialogue = dialoguetxt(env, phone, pid, file)
    dialogue.testcase()


if __name__ == '__main__':
    run()
    # i = 0
    # while i < 5:
    #     i = i + 1
    #     run()

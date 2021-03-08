# -*- coding: utf-8 -*-
from case.test_json.dialoguewithtxt import dialoguetxt

"""
顺丰全场景 txt测试。
"""


def run():
    phone = '1026'
    pid = "914008023"
    env = 'prod'
    file = "test"
    dialogue = dialoguetxt(env, phone, pid, file, checklabel=None)
    dialogue.testcase()


if __name__ == '__main__':
    run()
    # i = 0
    # while i < 5:
    #     i = i + 1
    #     run()

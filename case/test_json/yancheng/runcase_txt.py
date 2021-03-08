# -*- coding: utf-8 -*-
from case.test_json.pubshjson import generatejson_push
from case.test_json.dialoguewithtxt import dialoguetxt


def run_txt():
    pass
    phone = '1028'
    pid = "914012217"
    # pid="914007918"
    pid = "914012693"
    mobilephone = '18513583959'
    # env = 'test'
    env = 'alpha'
    # env = 'beta'
    # env='prod'
    file = "test"
    file = "社保"
    # file = "test2"
    # file = "特殊处理"
    pushdeppon = False
    randphone = False
    # randphone = True
    checklable = {"is_benren": "是否本人", "is_busy": "是否忙碌", "reason": "不贷款原因", "reduce": "降低利率是否会贷款",
                  "require": "是否有贷款需求",
                  "amount": "期望贷款金额", "is_zhuangao": "是否代为转告"}
    checklable = {
        "is_receive": "是否收到社保卡"
    }
    # checklable = None
    dialogue = dialoguetxt(env, phone, pid, file, checklabel=checklable)
    dialogue.testcase()


if __name__ == '__main__':
    run_txt()
    # pushjson()

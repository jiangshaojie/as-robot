# -*- coding: utf-8 -*-
from case.test_json.dialogtest import runcase
from case.test_json.getjson import SynJson
from case.test_json.pubshjson import generatejson_push
from case.test_json.pubshjson import push
from datetime import datetime
from case.test_json.addinent import publish2
from case.test_json.addinent import publish
import json

""""
自由发挥
"""


def run():
    # randphone = True
    pid = "914008023"
    env = "beta"
    publish(pid, env)
    betapushjson_daytime()
    case = "biguiyuan.xlsx"
    sheetnames = ["ivr"]
    runcase(case, threadnum=10, sheetnames=sheetnames)
    betapushjson_nighttime()
    sheetnames = ["夜间ivr"]
    runcase(case, threadnum=10, sheetnames=sheetnames)


def betapushjson_daytime():
    botname = "碧桂园智能IVR"
    synjson = SynJson(botname)
    synjson.getjson()
    env = "beta"
    hour = datetime.now().hour
    if hour < 8:
        time_str = [str(hour) + ":00", "22:00"]
    if hour >= 22:
        time_str = ["08:00", "24:00"]
    if 8 <= hour < 22:
        time_str = ["08:00", "22:00"]
    generatejson_push(botname, env, biguiyuan_time=json.dumps(time_str))


def betapushjson_nighttime():
    botname = "碧桂园智能IVR"
    # synjson = SynJson(botname)
    # synjson.getjson()
    env = "beta"
    hour = datetime.now().hour
    if hour < 22:
        time_str = ["08:00", str(hour) + ":00"]
    if hour >= 22:
        time_str = ["08:00", "22:00"]
    generatejson_push(botname, env, biguiyuan_time=json.dumps(time_str))


def pushbot():
    with open("碧桂园智能IVR_1577950568901.json", "r", encoding="UTF-8") as file:
        bot = json.load(file)
    # print(bot)
    env = "dev"
    re = push(env, bot)
    print(re.text)


def conditions():
    with open("碧桂园智能IVR", "r", encoding="UTF-8") as file:
        bot = json.load(file)
        botflows = \
            bot["botFlows"][0]["botFlowStartNode"]["transitionControls"][0]["flowCondition"]["conditions"][0][
                "conditions"][
                0]["operands"][0]
        print(botflows)

    # env = "dev"
    # re = push(env, bot)
    # print(re.text)


if __name__ == '__main__':
    # betapushjson_daytime()
    # betapushjson_nighttime()
    run()
    # pushbot()
    # conditions()

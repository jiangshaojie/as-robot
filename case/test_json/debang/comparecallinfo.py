# -*- coding: utf-8 -*-
import json
import datetime
import uuid
import re
import time
from random import random
from jsonschema import validate
import random
from case.test_json.dialoguewithtxt import dialoguetxt

baenv = {
    'test': 'http://nlu-test.talkinggenie.com/dataclean/message/yto/messages/v2',
    'alpha': 'http://nlu-alpha.talkinggenie.com/dataclean/message/yto/messages/v2',
    'beta': 'http://debugcheck-beta.talkinggenie.com/dataclean/message/yto/messages/v2',
    'prod': 'http://nlu.talkinggenie.com/dataclean/message/yto/messages/v2',
}


def compare(env):
    dialogue = dialoguetxt(env=env, phone=None, pid=None, casetxt=None)
    pid = "914006674"
    # "17:30:00"
    timekeeper = datetime.datetime.now().strftime("%H:%M:%S")
    if timekeeper > "17:30:00":
        casefile = "debangcase_offhours.json"

    else:
        casefile = "debangcase_officehours.json"
    with open(casefile, "r", encoding="utf-8") as datafile:
        data = json.load(datafile)
    cases = data["data"]
    sessonids = []
    starttime = int(time.time() * 1000) - 3000
    for case in cases:
        phone = ""
        senderId = ""
        sessionId = ""
        for param in case["dialogue"]:
            print("param: ", str(param))
            if param["query"] == 'false':
                uustr = str(uuid.uuid1()).replace('-', '')
                phone = getphonenum()
                param['callNum'] = phone
                senderId = phone + '&' + uustr
                sessionId = uustr
                sessonids.append(sessionId)
                case["senderId"] = senderId
                case["sessionId"] = sessionId
            else:
                param['callNum'] = phone
            if param['query'] == 'false':
                param['command'] = "1"
            if param.get('command') is None:
                param["command"] = "0"
            print("param end is:", str(param))
            time.sleep(0.1)  # 等待1秒防止smart-dm-inter-boot 通话明细混乱
            dialogue.postba(senderId, sessionId, pid, baenv[env], param)
            del param["command"]
    print("data is: ", json.dumps(data, ensure_ascii=False))
    endtime = int(time.time() * 1000) + 5000  # 日志截止时间延迟5秒
    time.sleep(25)  # 等待25s日志进入es
    callinfo = dialogue.pushDepponCallInfo(endtime, starttime)
    for sessionid in sessonids:
        print("callinfo keys is: {}".format(callinfo.keys()))
        if callinfo.keys().__contains__(sessionid):
            pass
        else:
            print("callinfo not contain : {}".format(sessionid))
            time.sleep(5)
            callinfo = dialogue.pushDepponCallInfo(endtime, starttime)
    for case in cases:
        try:
            case["callinfo"] = json.loads(callinfo.get(case["sessionId"]).split("action", 1)[1])
        except:
            print("{}：日志对话明细未找到".format(case["sessionId"]))
            case["callinfo"] = ""

    comparefiled = ["serviceType", "normalEndIs", "sceneInfos", "sceneCount", "repeatCallIs", "callEndType",
                    "isArtificial", "channelSource", "funName", "interactions"]
    # checkfiled=[]
    schema = {
        "properties": {
            "startTime": {
                "type": "integer"
            },
            "endTime": {
                "type": "integer"
            },
            "caller": {
                "type": "string"
            },
            "recordNum": {
                "type": "string"
            },
            "recordingTime": {
                "type": "integer"
            },
            "callNumHoneLocation":{
                "type": "string"
            }
        },
        "required": [
            "startTime", "endTime", "caller", "recordNum", "recordingTime","callNumHoneLocation"
        ]
    }
    for case in cases:
        print("待对比处理的sessionid: {} 与 callinfo: {}".format(case["sessionId"], case["callinfo"]))
        flag = True
        comfiledre = []
        if case["callinfo"] == "":
            flag = False
        else:
            for filed in comparefiled:
                print("待对比filed: {}".format(filed))
                print("待对比case： {}".format(case["callinfo"][filed]))
                print("待对比callrecordexpect: {}".format(case["callrecordexpect"][filed]))
                # if re.sub('\d{4}', "", case["callinfo"][filed]) == re.sub('\d{4}', "", case["callrecordexpect"][filed]):
                if case["callinfo"][filed] == case["callrecordexpect"][filed]:
                    pass
                else:
                    flag = False
                    comfiledre.append(filed)
            if case["callinfo"]["caller"] is None:
                comfiledre.append("caller")
                flag = False
            if case["callinfo"]["endTime"] > case["callinfo"]["startTime"]:
                pass
            else:
                comfiledre.append("endTime")
                flag = False
            try:
                validate(case["callinfo"],schema)
            except BaseException:
                flag=False
                comfiledre.append("schema")
        case["compareresult"] = flag
        case["comre"] = comfiledre

    with open("debangcase_result.json", "w", encoding="utf-8") as rfile:
        json.dump(data, rfile, ensure_ascii=False, indent=1)
    with open("compareresult.txt", "w", encoding="UTF-8") as refile:
        for case in cases:
            if case["compareresult"] == False:
                print(case["name"] + " 没有通过")
                refile.write(case["name"] + " 没有通过")
                refile.write("\n")
                print("结果：" + json.dumps(case, ensure_ascii=False))
                refile.write("结果：" + "\n")
                refile.write(json.dumps(case, ensure_ascii=False))
                refile.write("\n")


def getphonenum():
    phoneset = []

    phone = getphone()
    # if phoneset.count(phone)>0:
    print(phoneset.count(phone) > 0)
    while phoneset.count(phone) > 0:
        phone = getphone()
    phoneset.append(phone)
    return phone


def getphone():
    number = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    n = 0
    tailnum = ""
    while (n < 4):
        n += 1
        tailnum += str(random.choice(number))
    phone = "185" + str(
        str(int(time.time() * 10))[-4:] + tailnum)
    return phone


if __name__ == '__main__':
    env = "alpha"
    compare(env)

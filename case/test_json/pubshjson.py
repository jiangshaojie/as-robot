# -*- coding: utf-8 -*-
import time
import json
import requests
from case.test_json.getjson import SynJson
from case.test_json.addinent import publish
from case.test_json.addinent import publish2


def methodmodify(jsonobject, modfiy, **kwargs):
    """
    :param jsonobject:
    :param modfiy:
    :return:返回修改后的json
    """
    print("kwargs 参数为： ", kwargs)
    if modfiy:
        # 修改 operationFunctions
        if modfiy.get("operationFunctions"):
            operationFunctions = jsonobject["operationFunctions"]
            for item in modfiy.get("operationFunctions"):
                for method in operationFunctions:
                    if item.get("name") == method.get("name"):
                        del item["name"]
                        for k, v in item.items():
                            method[k] = v
            jsonobject["operationFunctions"] = operationFunctions
        # 修改botVariables
        if modfiy.get("botVariables"):
            botVariables = jsonobject["botVariables"]
            for item in modfiy.get("botVariables"):
                for variable in botVariables:
                    if item.get("variableName") == variable.get("variableName"):
                        del item["variableName"]
                        for k, v in item.items():
                            variable[k] = v
            jsonobject["botVariables"] = botVariables
    if kwargs.get("manual"):
        botFlows = jsonobject["botFlows"]
        for botFlow in botFlows:
            if botFlow.get("botFlowName") == "下单new":
                botFlowNodes = botFlow["botFlowNodes"]
                for botFlowNode in botFlowNodes:
                    if botFlowNode.get("nodeName") == "判断是否在截单时间":
                        botFlowNode.get("transitionControls")[0].get("flowCondition")["conditions"][0].get("operands")[
                            0] = "#between(#parseInt(#systimeFmt('HHmm')),#parseJsonArray('[900," + kwargs.get(
                            "manual") + "]'))"
                        break
                botFlow["botFlowNodes"] = botFlowNodes
        jsonobject["botFlows"] = botFlows
    if kwargs.get("manual_reservation"):
        botFlows = jsonobject["botFlows"]
        for botFlow in botFlows:
            if botFlow.get("botFlowName") == "下单new":
                botFlowNodes = botFlow["botFlowNodes"]
                for botFlowNode in botFlowNodes:
                    if botFlowNode.get("nodeName") == "判断是否在截单时间":
                        # 修改前值时间
                        botFlowNode.get("transitionControls")[0].get("flowCondition")["conditions"][0].get("operands")[
                            0] = "#between(#parseInt(#systimeFmt('HHmm')),#parseJsonArray('[900," + kwargs.get(
                            "manual_reservation") + "]'))"
                        # 修改后值时间
                        botFlowNode.get("transitionControls")[1].get("flowCondition")["conditions"][0].get("operands")[
                            0] = "#between(#parseInt(#systimeFmt('HHmm')),#parseJsonArray('[" + kwargs.get(
                            "manual_reservation") + ",2400]'))"
                        break
                botFlow["botFlowNodes"] = botFlowNodes
        jsonobject["botFlows"] = botFlows
    if kwargs.get("biguiyuan_time"):
        botFlows = jsonobject["botFlows"]
        botFlows[0]["botFlowStartNode"]["transitionControls"][0]["flowCondition"]["conditions"][0]["conditions"][0][
            "operands"][
            0] = """#between(#systimeFmt('HH:mm'),#parse('""" + kwargs.get("biguiyuan_time") + """','list'))"""
        jsonobject["botFlows"] = botFlows
    if kwargs.get("debang_order"):
        botFlows = jsonobject["botFlows"]
        botFlows[5]["botFlowNodes"][18]["transitionControls"][2]["flowCondition"]["conditions"] = [
            {
                "operands": [
                    "#between(#parseInt(#systimeFmt('yyyyMMddHH')),#parseJsonArray('[2021012600,2021020922]'))"
                ],
                "__leftVal": "manual",
                "__value": "#between(#parseInt(#systimeFmt('yyyyMMddHH')),#parseJsonArray('[2021012600,2021020922]'))"
            }
        ]
        jsonobject["botFlows"] = botFlows
    if kwargs.get("debang_fesival"):
        if kwargs.get("debang_fesival") == "middle":
            nlgTemplates = jsonobject["nlgTemplates"]
            # conditionDialogs=nlgTemplates["node-75598bd6-0934-4f06-b49d-21e40b3861e8"]["conditionDialogs"]

            # nlgTemplates["node-75598bd6-0934-4f06-b49d-21e40b3861e8"]["conditionDialogs"][0]["dialogs"][0][
            #     "templateName"] = "node-75598bd6-0934-4f06-b49d-21e40b3861e8__bc093235-0591-47ba-a9c8-c2cafad0f1ad"
            nlgTemplates["node-75598bd6-0934-4f06-b49d-21e40b3861e8"]["conditionDialogs"][0]["dialogs"][0][
                "templateName"], \
            nlgTemplates["node-75598bd6-0934-4f06-b49d-21e40b3861e8"]["conditionDialogs"][1]["dialogs"][0][
                "templateName"] = \
            nlgTemplates["node-75598bd6-0934-4f06-b49d-21e40b3861e8"]["conditionDialogs"][1]["dialogs"][0][
                "templateName"], \
            nlgTemplates["node-75598bd6-0934-4f06-b49d-21e40b3861e8"]["conditionDialogs"][0]["dialogs"][0][
                "templateName"]

            nlgTemplates["node-e85b4cf0-11a0-4e6a-bc02-a9fb8291e2dc"]["conditionDialogs"][0]["dialogs"][0][
                "templateName"], \
            nlgTemplates["node-e85b4cf0-11a0-4e6a-bc02-a9fb8291e2dc"]["conditionDialogs"][1]["dialogs"][0][
                "templateName"] = \
                nlgTemplates["node-e85b4cf0-11a0-4e6a-bc02-a9fb8291e2dc"]["conditionDialogs"][1]["dialogs"][0][
                    "templateName"], \
                nlgTemplates["node-e85b4cf0-11a0-4e6a-bc02-a9fb8291e2dc"]["conditionDialogs"][0]["dialogs"][0][
                    "templateName"]

            jsonobject["nlgTemplates"] = nlgTemplates
    if kwargs.get("debang_fesival"):
        if kwargs.get("debang_fesival") == "end":
            nlgTemplates = jsonobject["nlgTemplates"]
            # conditionDialogs=nlgTemplates["node-75598bd6-0934-4f06-b49d-21e40b3861e8"]["conditionDialogs"]

            # nlgTemplates["node-75598bd6-0934-4f06-b49d-21e40b3861e8"]["conditionDialogs"][0]["dialogs"][0][
            #     "templateName"] = "node-75598bd6-0934-4f06-b49d-21e40b3861e8__872a0f3c-612e-4a68-b96c-12ca6fb5640a"
            nlgTemplates["node-75598bd6-0934-4f06-b49d-21e40b3861e8"]["conditionDialogs"][0]["dialogs"][0][
                "templateName"], \
            nlgTemplates["node-75598bd6-0934-4f06-b49d-21e40b3861e8"]["conditionDialogs"][2]["dialogs"][0][
                "templateName"] = \
                nlgTemplates["node-75598bd6-0934-4f06-b49d-21e40b3861e8"]["conditionDialogs"][2]["dialogs"][0][
                    "templateName"], \
                nlgTemplates["node-75598bd6-0934-4f06-b49d-21e40b3861e8"]["conditionDialogs"][0]["dialogs"][0][
                    "templateName"]

            nlgTemplates["node-e85b4cf0-11a0-4e6a-bc02-a9fb8291e2dc"]["conditionDialogs"][0]["dialogs"][0][
                "templateName"], \
            nlgTemplates["node-e85b4cf0-11a0-4e6a-bc02-a9fb8291e2dc"]["conditionDialogs"][2]["dialogs"][0][
                "templateName"] = \
                nlgTemplates["node-e85b4cf0-11a0-4e6a-bc02-a9fb8291e2dc"]["conditionDialogs"][2]["dialogs"][0][
                    "templateName"], \
                nlgTemplates["node-e85b4cf0-11a0-4e6a-bc02-a9fb8291e2dc"]["conditionDialogs"][0]["dialogs"][0][
                    "templateName"]
            jsonobject["nlgTemplates"] = nlgTemplates
    if kwargs.get("debang_fesival"):
        if kwargs.get("debang_fesival") == "out":
            nlgTemplates = jsonobject["nlgTemplates"]
            # conditionDialogs=nlgTemplates["node-75598bd6-0934-4f06-b49d-21e40b3861e8"]["conditionDialogs"]

            # nlgTemplates["node-75598bd6-0934-4f06-b49d-21e40b3861e8"]["conditionDialogs"][0]["dialogs"][0][
            #     "templateName"] = "node-75598bd6-0934-4f06-b49d-21e40b3861e8__72bc29ab-4b68-4dd8-b189-928c47b49d30"

            nlgTemplates["node-75598bd6-0934-4f06-b49d-21e40b3861e8"]["conditionDialogs"][0]["dialogs"][0][
                "templateName"], \
            nlgTemplates["node-75598bd6-0934-4f06-b49d-21e40b3861e8"]["conditionDialogs"][3]["dialogs"][0][
                "templateName"] = \
                nlgTemplates["node-75598bd6-0934-4f06-b49d-21e40b3861e8"]["conditionDialogs"][3]["dialogs"][0][
                    "templateName"], \
                nlgTemplates["node-75598bd6-0934-4f06-b49d-21e40b3861e8"]["conditionDialogs"][0]["dialogs"][0][
                    "templateName"]
            # nlgTemplates["node-e85b4cf0-11a0-4e6a-bc02-a9fb8291e2dc"]["conditionDialogs"][0]["dialogs"][0][
            #     "templateName"], \
            # nlgTemplates["node-e85b4cf0-11a0-4e6a-bc02-a9fb8291e2dc"]["conditionDialogs"][3]["dialogs"][0][
            #     "templateName"] = \
            #     nlgTemplates["node-e85b4cf0-11a0-4e6a-bc02-a9fb8291e2dc"]["conditionDialogs"][3]["dialogs"][0][
            #         "templateName"], \
            #     nlgTemplates["node-e85b4cf0-11a0-4e6a-bc02-a9fb8291e2dc"]["conditionDialogs"][0]["dialogs"][0][
            #         "templateName"]

            jsonobject["nlgTemplates"] = nlgTemplates
    return jsonobject


def botvresionmodify(jsonobject):
    jsonobject["botVersion"] = str(int(time.time() * 1000))
    return jsonobject


def generatejson_push(file, env, modfiy=None, importintent=None, **kwargs):
    if env.lower() == "prod":
        raise Exception("禁止操作同步到prod环境")
    synjson = SynJson(file)
    synjson.getjson()
    with open(file, "r", encoding="utf-8") as f:
        jsonobject_init = json.load(f)
        botName = jsonobject_init["botName"]
        botVersion = jsonobject_init["botVersion"]
        jsonobject = botvresionmodify(jsonobject_init)
        # if modfiy is None:
        #     pass
        # else:
        jsonobject = methodmodify(jsonobject, modfiy, **kwargs)
    filename = file.replace("\\", "/").split("/")[-1]
    resultname = filename.split(".")[0] + "_" + env + ".json"
    with open(resultname, "w", encoding="utf-8") as re:
        json.dump(jsonobject, re, ensure_ascii=False, indent=4)
    # 记录对应环境发布版本
    with open("changelist_" + env, "a", encoding="utf-8") as changinfo:
        changinfo.write("botname: {} , version: {} ,发布时间：{}, 更新时间: {}".format(botName,
                                                                              botVersion,
                                                                              time.strftime("%Y-%m-%d %H:%M:%S",
                                                                                            time.localtime(
                                                                                                int(botVersion[:-3]))),
                                                                              time.strftime("%Y-%m-%d %H:%M:%S",
                                                                                            time.localtime())))
        changinfo.write("\n")
    # 调整顺序先同步话术，后同步意图。在同步bot
    pid = jsonobject["pid"]
    synjson.synchronsizedata(pid, env)  # 同步话术
    if importintent:
        if importintent.lower() == "v1":
            publish(pid, env)  # 发布定制意图
        if importintent.lower() == "v2":
            publish2(pid, env)

    n = 1
    for i in range(3):
        print("第 {} 次同步bot".format(n))
        re = push(env, jsonobject)  # 发布json
        responsecode = json.loads(re.text).get("code")
        if responsecode == 200:
            break
        n = n + 1
    if responsecode == 200:
        print("{} 同步到 {} 成功".format(file, env))
    else:
        raise Exception("{} 同步到 {} 失败".format(file, env))


def generatejson_push_sf(file, env, modfiy=None, importintent=None, **kwargs):
    if env.lower() == "prod":
        raise Exception("禁止操作同步到prod环境")
    synjson = SynJson(file)
    synjson.getjson()
    with open(file, "r", encoding="utf-8") as f:
        jsonobject_init = json.load(f)
        botName = jsonobject_init["botName"]
        botVersion = jsonobject_init["botVersion"]
        jsonobject = botvresionmodify(jsonobject_init)
        if modfiy is None:
            pass
        else:
            jsonobject = methodmodify(jsonobject, modfiy, **kwargs)
    filename = file.replace("\\", "/").split("/")[-1]
    resultname = filename.split(".")[0] + "_" + env + ".json"
    with open(resultname, "w", encoding="utf-8") as re:
        json.dump(jsonobject, re, ensure_ascii=False, indent=4)
    # 记录对应环境发布版本
    with open("changelist_" + env, "a", encoding="utf-8") as changinfo:
        changinfo.write("botname: {} , version: {} ,发布时间：{}, 更新时间: {}".format(botName,
                                                                              botVersion,
                                                                              time.strftime("%Y-%m-%d %H:%M:%S",
                                                                                            time.localtime(
                                                                                                int(botVersion[:-3]))),
                                                                              time.strftime("%Y-%m-%d %H:%M:%S",
                                                                                            time.localtime())))
        changinfo.write("\n")

    # responsecode = json.loads(re.text).get("code")
    number = 1
    for i in range(3):
        re = push(env, jsonobject)  # 发布json
        print("第 {} 次同步".format(number))
        responsecode = json.loads(re.text).get("code")
        if responsecode == 200:
            break
        number = number + 1
    if responsecode == 200:
        print("{} 同步到 {} 成功".format(file, env))
    else:
        raise Exception("{} 同步到 {} 失败".format(file, env))


def loaljson_push(file, env, modfiy=None, importintent=None):
    if env.lower() == "prod":
        raise Exception("禁止操作同步到prod环境")
    synjson = SynJson(file)
    # synjson.getjson()
    with open(file, "r", encoding="utf-8") as f:
        jsonobject_init = json.load(f)
        botName = jsonobject_init["botName"]
        botVersion = jsonobject_init["botVersion"]
        jsonobject = botvresionmodify(jsonobject_init)
        if modfiy is None:
            pass
        else:
            jsonobject = methodmodify(jsonobject, modfiy)
    filename = file.replace("\\", "/").split("/")[-1]
    resultname = filename.split(".")[0] + "_" + env + ".json"
    with open(resultname, "w", encoding="utf-8") as re:
        json.dump(jsonobject, re, ensure_ascii=False, indent=4)
    # 记录对应环境发布版本
    with open("changelist_" + env, "a", encoding="utf-8") as changinfo:
        changinfo.write("botname: {} , version: {} ,发布时间：{}, 更新时间: {}".format(botName,
                                                                              botVersion,
                                                                              time.strftime("%Y-%m-%d %H:%M:%S",
                                                                                            time.localtime(
                                                                                                int(botVersion[:-3]))),
                                                                              time.strftime("%Y-%m-%d %H:%M:%S",
                                                                                            time.localtime())))
        changinfo.write("\n")
    re = push(env, jsonobject)  # 发布json
    responsecode = json.loads(re.text).get("code")
    if responsecode == 200:
        print("{} 同步到 {} 成功".format(file, env))
    else:
        raise Exception("{} 同步到 {} 失败".format(file, env))
    pid = jsonobject["pid"]
    synjson.synchronsizedata(pid, env)  # 同步话术
    if importintent.lower() == "v1":
        publish(pid, env)  # 发布定制意图
    if importintent.lower() == "v2":
        publish2(pid, env)


def push(env, jsonobject):
    """
    发到env bot并返回发布结果
    :param env:
    :param jsonobject:
    :return:
    """
    url = {
        "test": "http://s-gateway.t.talkinggenie.com/smart/dm/loader/v1/publish",
        # "beta": "http://s-gateway-beta.talkinggenie.com/smart/dm/loader/v1/publish",
        "beta": "https://beta.talkinggenie.com/api/v2/smart/dm/loader/v1/publish",
        "alpha": "http://s-gateway-alpha.talkinggenie.com/smart/dm/loader/v1/publish",
        "dev": "http://s-gateway.dev.talkinggenie.com/smart/dm/loader/v1/publish"
    }
    header = {
        "Content-Type": "application/json"
    }
    print("push url: {}".format(url[env]))
    re = requests.post(url[env], json=jsonobject, headers=header)
    print(re.text)
    return re


if __name__ == '__main__':
    pid = "914008023"
    env = "beta"
    # synchronsizedata(pid, env)
    publish(pid, env)

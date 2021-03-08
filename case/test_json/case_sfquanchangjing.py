# -*- coding: utf-8 -*-
from case.test_json.dialogtest import runcase
from case.test_json.dialogtest import run_data
from case.test_json.pubshjson import generatejson_push
from case.test_json.pubshjson import generatejson_push_sf
from case.test_json.getjson import SynJson
from case.test_json.addinent import publish2
from case.test_json.pubshjson import push
from case.test_json.pubshjson import botvresionmodify
import datetime
# from datetime import datetime
import json
import requests

""""
下单流程：快递下单地址V4
"""


def run():
    """
    transernum_servicetype 检查transernum_servicetype
    servicetype 检查 servicetype
    :return:
    """
    # randphone = True
    env = "beta"
    pid = "914009574"
    pid = pid
    botname = "顺丰物流全场景机器人"

    synjson = SynJson(botname)
    synjson.synchronsizedata(pid, env)  # 同步话术

    publish2(pid, env)  # 同步前端定制意图。先暂时注释掉

    # case1
    updatePeakConfig(isPeakTime=False)  # 关闭高峰策略  注意 smart-robot-config 版本
    betapushjson(env)  # 先暂时注释掉
    case = "sf_quanchangjing.xlsx"
    sheetnames = ["查单", "通用流程", "拒收", "催单", "ivr", "转人工组别", "开发票", "修改收方信息", "退回", "特殊查单", "快件损坏", "下单", "查询网点", "价格咨询",
                  "asr回拨", "取消下单", "投诉"]
    runcase(case, sheetnames=sheetnames, threadnum=15, check_topic_type="servicetype")

    # case2截单测试

    betapushjson_reservation(env)  # 先暂时注释掉
    sheetnames = ["截单测试"]
    runcase(case, sheetnames=sheetnames, threadnum=10, check_topic_type="servicetype")

    # 高峰管控测试
    isPeakTime(case)


def isPeakTime(case=None):
    if not case:
        case = "sf_quanchangjing.xlsx"
    # 开启，会员开启，等级：会员，下单，查单 均设置两次
    updatePeakConfig(isPeakTime=True)
    sheetnames = ["高峰管控1"]
    runcase(case, sheetnames=sheetnames, threadnum=15, check_topic_type="servicetype")
    updatePeakConfig(isPeakTime=True, memberLevelSwitch=0)  # 开启，会员关闭，首节点、查单 均两次
    sheetnames = ["高峰管控2"]
    runcase(case, sheetnames=sheetnames, threadnum=15, check_topic_type="servicetype")
    updatePeakConfig(isPeakTime=True, memberLevelSwitch=1, memberLevel="0", queryOrderFlowRepeatTimes=1,
                     firstNodeRepeatTimes=1)  # 开启，会员开始，等级：非会员 ，首节点、查单 均一次
    sheetnames = ["高峰管控3"]
    runcase(case, sheetnames=sheetnames, threadnum=15, check_topic_type="servicetype")
    updatePeakConfig(isPeakTime=True, memberLevelSwitch=1, memberLevel="1", queryOrderFlowRepeatTimes=1,
                     firstNodeRepeatTimes=1)  # 开启，会员开始，等级：会员，首节点，查单 均一次
    sheetnames = ["高峰管控4"]
    runcase(case, sheetnames=sheetnames, threadnum=15, check_topic_type="servicetype")
    updatePeakConfig(isPeakTime=True, memberLevelSwitch=0, queryOrderFlowRepeatTimes=1,
                     firstNodeRepeatTimes=1)  # 开启，会员关闭，首节点、查单 均一次
    sheetnames = ["高峰管控5"]
    runcase(case, sheetnames=sheetnames, threadnum=15, check_topic_type="servicetype")
    updatePeakConfig(isPeakTime=True, memberLevelSwitch=1, memberLevel="0", queryOrderFlowRepeatTimes=2,
                     firstNodeRepeatTimes=2)  # 开启，会员开始，等级：非会员 ，首节点、查单 均两次
    sheetnames = ["高峰管控6"]
    runcase(case, sheetnames=sheetnames, threadnum=15, check_topic_type="servicetype")


def betapushjson(env):
    botname = "顺丰物流全场景机器人"
    if env == "beta":
        modfiy = {

            "operationFunctions": [{"name": "node-f79983df-b633-4d2d-8299-b936cdd68352",
                                    "uri": "http://10.32.2.209:8091/inter/api/v1/sf/queryComplaintCount"
                                    },
                                   {"name": "node-153e3292-1f93-4baf-9191-05cc679003bb",
                                    "uri": "http://10.32.2.209:8091/inter/api/v1/sf/judgeIvr"},
                                   {"name": "node-d6a44c3d-7215-4611-b90e-8e2b4de0235e",
                                    "uri": "http://10.32.2.209:8091/inter/api/v1/sf/statStartNodeTransfer"},
                                   {"name": "node-a8ce196d-50f0-43d6-9c68-a776dfd69c28",
                                    "uri": "http://10.32.2.209:8091/inter/api/v1/sf/judgeConsultIsLarger"}
                                   ]
        }
    if env == "test":
        modfiy = {

            "operationFunctions": [{"name": "node-f79983df-b633-4d2d-8299-b936cdd68352",
                                    "uri": "http://10.12.6.75:8091/inter/api/v1/sf/queryComplaintCount"
                                    },
                                   {"name": "node-153e3292-1f93-4baf-9191-05cc679003bb",
                                    "uri": "http://10.12.6.75:8091/inter/api/v1/sf/judgeIvr"},
                                   {"name": "node-d6a44c3d-7215-4611-b90e-8e2b4de0235e",
                                    "uri": "http://10.12.6.75:8091/inter/api/v1/sf/statStartNodeTransfer"},
                                   {"name": "node-a8ce196d-50f0-43d6-9c68-a776dfd69c28",
                                    "uri": "http://10.12.6.75:8091/inter/api/v1/sf/judgeConsultIsLarger"}
                                   ]
        }
    # manual = "1900"
    hour = datetime.datetime.now().hour
    if hour < 18:
        generatejson_push_sf(botname, env, modfiy, importintent="v2")
    else:
        manual_h = str(int(hour) + 1) + "00"
        generatejson_push_sf(botname, env, modfiy, importintent="v2", manual=manual_h)


def betapushjson_reservation(env):
    botname = "顺丰物流全场景机器人"
    # env = "beta"
    if env == "beta":
        modfiy = {

            "operationFunctions": [{"name": "node-f79983df-b633-4d2d-8299-b936cdd68352",
                                    "uri": "http://10.32.2.209:8091/inter/api/v1/sf/queryComplaintCount"
                                    },
                                   {"name": "node-153e3292-1f93-4baf-9191-05cc679003bb",
                                    "uri": "http://10.32.2.209:8091/inter/api/v1/sf/judgeIvr"},
                                   {"name": "node-d6a44c3d-7215-4611-b90e-8e2b4de0235e",
                                    "uri": "http://10.32.2.209:8091/inter/api/v1/sf/statStartNodeTransfer"},
                                   {"name": "node-a8ce196d-50f0-43d6-9c68-a776dfd69c28",
                                    "uri": "http://10.32.2.209:8091/inter/api/v1/sf/judgeConsultIsLarger"}
                                   ]
        }
    if env == "test":
        modfiy = {

            "operationFunctions": [{"name": "node-f79983df-b633-4d2d-8299-b936cdd68352",
                                    "uri": "http://10.12.6.75:8091/inter/api/v1/sf/queryComplaintCount"
                                    },
                                   {"name": "node-153e3292-1f93-4baf-9191-05cc679003bb",
                                    "uri": "http://10.12.6.75:8091/inter/api/v1/sf/judgeIvr"},
                                   {"name": "node-d6a44c3d-7215-4611-b90e-8e2b4de0235e",
                                    "uri": "http://10.12.6.75:8091/inter/api/v1/sf/statStartNodeTransfer"},
                                   {"name": "node-a8ce196d-50f0-43d6-9c68-a776dfd69c28",
                                    "uri": "http://10.12.6.75:8091/inter/api/v1/sf/judgeConsultIsLarger"}
                                   ]
        }
    hour = datetime.datetime.now().hour
    if hour > 18:
        generatejson_push_sf(botname, env, modfiy, importintent="v2")
    else:
        manual_reservation = str(hour) + "00"
        generatejson_push_sf(botname, env, modfiy, importintent="v2", manual_reservation=manual_reservation)


def nlupushjson():
    """
    同步不修改下单时间判断的json
    :return:
    """
    botname = "顺丰物流全场景机器人"
    env = "beta"
    modfiy = {

        "operationFunctions": [{"name": "node-f79983df-b633-4d2d-8299-b936cdd68352",
                                # "uri": "http://10.12.6.75:8091/inter/api/v1/sf/queryComplaintCount"},
                                "uri": "http://10.32.2.209:8091/inter/api/v1/sf/queryComplaintCount"
                                },
                               {"name": "node-153e3292-1f93-4baf-9191-05cc679003bb",
                                "uri": "http://10.32.2.209:8091/inter/api/v1/sf/judgeIvr"},
                               {"name": "node-d6a44c3d-7215-4611-b90e-8e2b4de0235e",
                                "uri": "http://10.32.2.209:8091/inter/api/v1/sf/statStartNodeTransfer"},
                               {"name": "node-a8ce196d-50f0-43d6-9c68-a776dfd69c28",
                                "uri": "http://10.32.2.209:8091/inter/api/v1/sf/judgeConsultIsLarger"}
                               ]
    }

    pid = "914009574"
    synjson = SynJson(botname)
    synjson.synchronsizedata(pid, env)  # 同步话术
    generatejson_push(botname, env, modfiy, importintent="v2")
    # synjson = SynJson(botname)


def pushjson():
    env = "beta"
    with open("顺丰物流全场景机器人_beta.json", "r", encoding="utf-8") as jsonfile:
        bot = json.load(jsonfile)
        jsonobject = botvresionmodify(bot)
    re = push(env, jsonobject=jsonobject)
    print(re.text)


def initpush():
    botname = "顺丰物流全场景机器人"
    env = "beta"
    modfiy = {

        "operationFunctions": [{"name": "node-f79983df-b633-4d2d-8299-b936cdd68352",
                                "uri": "http://10.32.2.209:8091/inter/api/v1/sf/queryComplaintCount"
                                }
                               ]
    }
    # manual = "1900"
    hour = datetime.now().hour
    if hour < 18:
        generatejson_push_sf(botname, env, modfiy, importintent="v2")
    else:
        manual_h = str(int(hour) + 1) + "00"
        generatejson_push_sf(botname, env, modfiy, importintent="v2", manual=manual_h)


def push_importbot():
    botname = "通用电话号码收集"
    generatejson_push(botname, env="test")
    botname = "快递下单地址收集v4"
    generatejson_push(botname, env="test")


def updatePeakConfig(isPeakTime=None, **kwargs):
    # 参数默认会员等级开启，会员等级：会员，
    param = {
        "peakEndTime": "2021-11-11",
        "memberLevel": "1",
        "queryOrderFlowRepeatTimes": 2,
        "peakStartTime": "2020-10-30",
        "memberLevelSwitch": 1,
        "firstNodeRepeatTimes": 2
    }
    date = datetime.datetime.now()
    if isPeakTime:
        param["peakEndTime"] = date.strftime('%Y-%m-%d')
    if not isPeakTime:
        param["peakEndTime"] = (date - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    param.update(kwargs)
    print("高峰策略配置更新： ", param)
    url = "http://47.98.151.178:8091/inter/api/v1/sf/updatePeakConfig"
    # url = "http://s-gateway-beta.talkinggenie.com/sadmin/robot/api/v1/updatePeakConfig"
    re = requests.post(url=url, json=param)
    re_json = json.loads(re.text)
    if re_json.get("message") == "OK":
        print("高峰策略更新成功")
    else:
        print(re.text)
        raise Exception("高峰策略更新失败")


if __name__ == '__main__':
    run()
    # rundata()
    # nlupushjson()
    # isPeakTime()
    # betapushjson_reservation()
    # updatePeakConfig(isPeakTime=False)
    # updatePeakConfig(isPeakTime=True)  # 高峰1
    # updatePeakConfig(isPeakTime=True, memberLevelSwitch=1, memberLevel="1", queryOrderFlowRepeatTimes=1,firstNodeRepeatTimes=1)  #    高峰4
    # updatePeakConfig(isPeakTime=True, memberLevelSwitch=0) #高峰2
    # updatePeakConfig(isPeakTime=True, memberLevelSwitch=0, queryOrderFlowRepeatTimes=1,firstNodeRepeatTimes=1)  # 高峰5
    # updatePeakConfig(isPeakTime=True, memberLevelSwitch=1, memberLevel="0", queryOrderFlowRepeatTimes=1,firstNodeRepeatTimes=1) #高峰3

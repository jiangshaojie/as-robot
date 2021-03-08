# -*- coding: utf-8 -*-
import requests
import json
from requests_toolbelt import MultipartEncoder

addintenturl = {
    "beta": "http://debugcheckdirect-beta.talkinggenie.com/nlu-kf/dm/addIntent",
    "test": "http://debugcheckdirect-test.talkinggenie.com/nlu-kf/dm/addIntent"
}

nlu_dict_manager_url = {
    "beta": "http://debugcheckdirect-beta.talkinggenie.com/nlu-dict-manager/up-down-load-file/importZip",
    "test": "http://debugcheckdirect-test.talkinggenie.com/nlu-dict-manager/up-down-load-file/importZip"
}


def export(pid):
    url = 'http://internalofficeread.talkinggenie.com//nlu-kf/dm/exportScopeIntentList'
    data = {"pid": pid}
    headers = {
        "Content-Type": "application/json"
    }
    r = requests.post(url=url, json=data, headers=headers)
    return r


def export2(robotId):
    url = 'http://internalofficeread.talkinggenie.com/nlu-dict-manager/up-down-load-file/exportZip'
    data = {"robotId": robotId}
    headers = {
        "Content-Type": "application/json",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "*/*"
    }
    r = requests.post(url=url, json=data, headers=headers)
    if r.status_code != 200:
        print(r.text)
        raise Exception("导出V2意图失败")
    intentfilename = str(robotId) + ".exportintent"
    with open(intentfilename, "wb") as file:
        file.write(r.content)
    return intentfilename


def addintent(data, env):
    headers = {
        "Content-Type": "application/json"
    }
    url = addintenturl[env]
    r = requests.post(url=url, json=data, headers=headers)
    return r


def addintent2(filename, env):
    multipart_encoder = MultipartEncoder(
        {
            'file': ("file", open(filename, 'rb'), 'application/octet-stream')

        }
    )
    header = {
        'Content-Type': multipart_encoder.content_type
    }
    url = nlu_dict_manager_url[env]
    r = requests.post(url=url, data=multipart_encoder, headers=header)
    print("导入V2意图响应结果", r.status_code, r.text)
    if r.status_code != 200 or r.json().get("message") != "操作成功":
        raise Exception("导入V2意图失败", r)
    else:
        print("{} 环境导入V2意图成功".format(env))


def publish(pid, env):
    r = export(pid)
    print("V1意图导出："+r.text)
    if json.loads(r.text)["status"] == "200":
        intentlist = json.loads(r.text)["body"]
        for intent in intentlist:
            r = addintent(intent, env)
            if json.loads(r.text)["status"] == "200":
                print(r.text)
                print("意图： {}，添加成功".format(intent["name"]))
            else:
                print(r.text)
                raise Exception("意图： {}，添加失败".format(intent["name"]))
    else:
        raise Exception("{} 意图导出失败".format(pid))


def publish2(robotid, env):
    filename = export2(robotid)
    addintent2(filename, env)


if __name__ == '__main__':
    # pid = "914"
    # publish(pid)
    # robotid = 914009574
    # export2(robotid)
    addintent2("914009574.exportintent", "test")

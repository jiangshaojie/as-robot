# encoding:utf-8
import requests
import json
import uuid
from openpyxl import load_workbook
from openpyxl.styles import Font
from openpyxl.styles.colors import RED
from openpyxl.styles.colors import BLACK
from base.log import logger
import time
import shutil
from datetime import datetime
from random import random
import random
from case.test_json.acquirekibana import acquirekibana
import copy


class dialoguetxt():
    dmenv = {
        'alpha': 'http://dm-runtime-alpha.talkinggenie.com/callcenter/nlu',
        'prod': 'http://dm-runtime.talkinggenie.com/callcenter/nlu',
        'test': 'http://dm-runtime-test.talkinggenie.com/callcenter/nlu',
        "beta": "http://dm-runtime-beta.talkinggenie.com/callcenter/nlu"
    }
    baenv = {
        'test': 'http://nlu-test.talkinggenie.com/dataclean/message/yto/messages/v2',
        'alpha': 'http://nlu-alpha.talkinggenie.com/dataclean/message/yto/messages/v2',
        'beta': 'http://debugcheck-beta.talkinggenie.com/dataclean/message/yto/messages/v2',
        'prod': 'http://nlu.talkinggenie.com/dataclean/message/yto/messages/v2',
    }
    sessonids = []
    starttime = ""

    def __init__(self, env, phone, pid, casetxt, checklabel=None, randphone=None, outbound=False, pushdeppon=False,
                 calloutparam=None):
        # self.url = self.dmenv[env]
        self.phone = phone
        self.pid = pid
        # self.testtype = testtype
        self.casetxt = casetxt
        # if self.testtype == "ba":
        self.url = self.baenv[env]
        # else:
        self.dmurl = self.dmenv[env]
        self.randphone = randphone
        self.checklable = checklabel
        self.env = env
        self.outbound = outbound
        self.pushdeppon = pushdeppon
        self.callout = calloutparam

    def getphonenum(self):
        phoneset = []

        phone = self.getphone()
        # if phoneset.count(phone)>0:
        print(phoneset.count(phone) > 0)
        while phoneset.count(phone) > 0:
            phone = self.getphone()
        phoneset.append(phone)
        return phone

    def getphone(self):
        number = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        n = 0
        tailnum = ""
        while (n < 4):
            n += 1
            tailnum += str(random.choice(number))
        phone = "185" + str(
            str(int(time.time() * 10))[-4:] + tailnum)
        return phone

    def postba(self, senderId, sessionId, pid, url, param, citycode):
        print('url is {}'.format(url))
        command = param['command']
        print("command: {}".format(command))
        # logger.info("command: {}".format(command))
        if command == "1":
            self.starttime = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        body = {
            "content": param['query'],
            "senderId": senderId,
            "externalSessionId": "",
            "productId": pid,
            "recordId": str(uuid.uuid1()).replace('-', ''),
            "expressNumber": "",
            "command": param['command'],
            "type": "1",
            "isPlaying": "false",
            "playing": {
                "content": "",
                "type": ""
            },
            "recordingFile": "",
            "startTime": self.starttime,
            "stopTime": datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),
            "asrConfidence": "1.0",
            "callNum": param['callNum'],
            "sessionId": sessionId,
            "outboundStartTime": "",
            "outboundEndTime": "",
            "outboundStatus": "",
            "destNumber": "",
            "hangupReason": "other",
            # "taskId": "2226",
            # "phoneId": "6553079"
            "cityCode": citycode,
            "flag":0
        }
        if self.outbound == True:
            body["taskId"] = "2226"
            body["phoneId"] = "6553079"

        result = requests.post(url=url, json=body)
        logger.info("senderId %s", senderId)
        logger.info("request %s", body)
        logger.info("status_code %d status_text %s" % (result.status_code, result.text))
        return result

    def postdm(self, senderId, sessionId, pid, url, param):
        print('url is {}'.format(url))
        body = {
            "sessionId": senderId,
            "senderId": sessionId,
            "asrConfidence": 1,
            "productId": pid,
            # "productId": "914008023",
            "query": param['query'],
            "message": {
                "callNum": param['callNum'],
                "inputNum": param['inputNum']
            }
        }
        result = requests.post(url=url, json=body)
        logger.info("senderId %s", senderId)
        logger.info("request %s", body)
        logger.info("status_code %d status_text %s" % (result.status_code, result.text))
        return result

    def getlabel(self, senderId, sessionId, pid, url, param):
        print('dmurl is {}'.format(url))
        lablecontent = {}
        body = {
            "senderId": senderId,
            "asrConfidence": 1.0,
            "productId": pid,
            "query": "signal=hangUp",
            "sessionId": sessionId,
            "robotId": pid,
            "message": {
                "relayNum": "",
                "phone": param['callNum'],
                "phoneId": "",
                "callNum": param['callNum'],
                "destNumber": "",
                "taskId": ""
            }
        }
        result = requests.post(url=url, json=body)
        logger.info("senderId %s", senderId)
        logger.info("request %s", body)
        logger.info("status_code %d status_text %s" % (result.status_code, result.text))
        try:
            originallabel = json.loads(result.text)["best"]["reply"]["message"]
        except:
            originallabel = {}
        voicetext = json.loads(result.text)["best"]["reply"]["voiceText"]
        try:
            topicCode = json.loads(result.text)["best"]["reply"]["topicCode"]
        except:
            topicCode = ""
        print("topicCode", topicCode)
        for label in self.checklable.keys():
            # originallabel = json.loads(labeldict.get(sessionid))
            # originallabel = labeldict.get(sessionid)
            if label in originallabel.keys():
                lablecontent[self.checklable[label]] = originallabel[label]
            else:
                lablecontent[self.checklable[label]] = "此标签不存在"

        # lables[sessionid] = copy.deepcopy(lablecontent)
        # lablecontent.clear()
        return lablecontent, voicetext, topicCode

    def postoutbound(self, senderId, sessionId, pid, url, callout):
        """
        发起外呼请求
        :param case:
        :return:
        """
        data = {
            "senderId": senderId,
            "sessionId": sessionId,
            "asrConfidence": 1,
            "productId": pid,
            # "query": "signal=newCall",
            "query":"signal=outbound",
            "sid":"e7422b68634b40838d35bd112914c172",
            "robotId":pid,
            "message": callout
        }
        data["message"]["appId"] = int(data["message"]["appId"])
        print("outbounder request is   ", json.dumps(data, ensure_ascii=False))
        outboundr = requests.post(url=url, json=data)
        print("outbounder status_code is ", outboundr.status_code)
        print("ourbounder response is ", outboundr.text)
        return outboundr

    @staticmethod
    def count_chinese(string):
        """
        检查整个字符串中文数量
        :param string: 需要检查的字符串
        :return: number
        """
        number = 0
        for ch in string:
            if u'\u4e00' <= ch <= u'\u9fff':
                # return True
                number = number + 1
        return number

    def testcase(self):
        """
        :param casetxt:
        :param phone:
        :param pid:
        :return:
        使用方式，
        ba:
            false|phone   #不对phone赋值，使用默认值
            query|command
            asr-silence|4
            number|3
            hangup|command  #2  即 0|2
            首问语默认给 command 1
            其它语句默认给 command 0
            可手动赋值，

        dm:
            signal=newCall|phone
            query
            signal=inputNum|num
            signal=silence
            hangup
        """
        re = []
        cases = []
        originalphone = self.phone
        pid = self.pid
        starttime = int(time.time() * 1000) - 3000
        # if self.testtype == 'ba':
        with open(self.casetxt, 'r', encoding='utf-8') as f:
            param = {}
            for i in f.readlines():
                case = i.strip().split(' ')[0]
                if case[0:3] == 'pid':
                    pid = i.split(':')[1].strip()
                else:
                    if case[0:1] == '#':
                        re.append((case,))
                    # if params = str(case).split('|')
                    else:
                        cases.append(case)
                        params = str(case).split('|')
                        if len(case) > 0:
                            if params[0].lower() == "signal=hangup":
                                result = self.getlabel(senderId, sessionId, pid, self.dmurl, param)
                                print("result", str(result))
                                re.append(("hangup", result[1], " ", result[2], "",""))
                                re.append(("标签值： ", json.dumps(result[0], ensure_ascii=False), "", "", "",""))
                            else:
                                if params[0].lower() == 'false':
                                    uustr = str(uuid.uuid1()).replace('-', '')
                                    if len(params) == 3:
                                        citycode = params[2]
                                    else:
                                        citycode = ""
                                    try:
                                        phone = params[1]
                                        if len(phone) == 0:
                                            phone = originalphone
                                    except:
                                        # phone = originalphone
                                        # param['callNum'] = phone
                                        if self.randphone == True:
                                            # pass
                                            # phone = "185" + str(
                                            #     str(int(time.time() * 10))[-4:] + self.gettailnum())
                                            phone = self.getphonenum()
                                        else:
                                            phone = originalphone
                                    param['callNum'] = phone
                                    senderId = phone + '&' + phone + uustr
                                    sessionId = phone + uustr
                                    self.sessonids.append(senderId)
                                param['query'] = params[0]
                                if param['query'].lower() == 'false':
                                    param['command'] = "1"
                                    param["query"] = "false"
                                if param["query"] == "asr-silence":
                                    param['command'] = "4"
                                if param["query"] == "hangup":
                                    param['command'] = "2"
                                    param["query"] == "0"
                                if "command" in param:
                                    pass
                                elif len(params) > 1:
                                    command = params[1]
                                    param['command'] = command
                                else:
                                    param['command'] = "0"
                                print(param)
                                if self.callout != None and param["query"] == "false":
                                    reoutbout = self.postoutbound(senderId, sessionId, pid, self.dmurl, self.callout)
                                    print("外呼请求结果：{}".format(reoutbout.text))
                                result = self.postba(senderId, sessionId, pid, self.url, param, citycode)
                                del param["command"]
                                try:
                                    # 应答语
                                    titleclown = json.loads(result.text)['voiceText'].strip()
                                except:
                                    titleclown = ' '

                                try:
                                    # topiccode
                                    topiccde = json.loads(result.text)["topicCode"]
                                except:
                                    topiccde = ' '

                                try:
                                    # pid
                                    productpid = json.loads(result.text)["productId"]
                                except:
                                    productpid = ' '
                                try:
                                    # transnum
                                    transferNum = json.loads(result.text)["transferNum"]
                                except:
                                    transferNum = ""

                                try:
                                    # transnum
                                    serviceType = json.loads(result.text)["serviceType"]
                                except:
                                    serviceType = ""

                                try:
                                    # ordernumber
                                    orderNum = json.loads(result.text)["orderNum"]
                                except:
                                    orderNum = ""

                                re.append((case, titleclown, productpid, topiccde, transferNum,serviceType,orderNum))


        # else:
        #     with open(self.casetxt, 'r', encoding='utf-8') as f:
        #         param = {}
        #         for i in f.readlines():
        #             case = i.strip().split(' ')[0]
        #             if case[0:3] == 'pid':
        #                 pid = i.split(':')[1].strip()
        #             else:
        #                 if case[0:1] == '#':
        #                     re.append((case,))
        #                 else:
        #                     cases.append(case)
        #                     params = str(case).split('|')
        #                     if len(case) > 0:
        #                         if params[0] == 'signal=newCall':
        #                             uustr = str(uuid.uuid1()).replace('-', '')
        #                             try:
        #                                 phone = params[1]
        #                                 param['callNum'] = phone
        #                             except:
        #                                 phone = originalphone
        #                                 param['callNum'] = phone
        #                             senderId = phone + '&' + uustr
        #                             sessionId = uustr
        #                         param['query'] = params[0]
        #                         if params[0] == 'signal=inputNum':
        #                             param['inputNum'] = params[1]
        #                         else:
        #                             param['inputNum'] = None
        #
        #                         result = self.postdm(senderId, sessionId, pid, self.url, param)
        #                         try:
        #                             # 应答语
        #                             titleclown = json.loads(result.text)['best']['reply']['voiceText'].strip()
        #                         except:
        #                             titleclown = ' '
        #
        #                         try:
        #                             # topiccode
        #                             topiccde = json.loads(result.text)["best"]["reply"]["topicCode"]
        #                         except:
        #                             topiccde = ' '
        #
        #                         try:
        #                             # pid
        #                             productpid = json.loads(result.text)["best"]["reply"]["pid"]
        #                         except:
        #                             productpid = ' '
        #
        #                         # try:
        #                         #     # pid
        #                         #     flow = json.loads(result.text)["best"]["reply"]["flow"]
        #                         # except:
        #                         #     flow = ' '
        #
        #                         re.append((case, titleclown, productpid, topiccde))
        # print("re is", re)
        logger.info("对话sessionid ：{}".format(self.sessonids))
        resulttxt = 'result_' + self.casetxt.split('/')[-1]
        endtime = int(time.time() * 1000) + 100000
        # if self.checklable is not None:
        #     lables = self.sessionslabels(endtime, starttime, self.sessonids, self.checklable)
        if self.pushdeppon:
            count = 1
            callinfo = self.pushDepponCallInfo(endtime, starttime)
            time.sleep(10)  # 等待10s日志进入es
            while len(callinfo) < len(self.sessonids):
                if count > 5:
                    raise Exception("获取的话单数量小于对话数量")
                time.sleep(5)
                callinfo = self.pushDepponCallInfo(endtime, starttime)
                print("第 {} 次请求 callinfo len{}: ".format(count, len(callinfo)))
                print("sessonids len: ", len(self.sessonids))
                count = count + 1

        with open(resulttxt, 'w', encoding='utf-8') as refile:
            index = 0
            for i in re:
                if len(i) == 1:
                    lines = '{}'.format(i[0])
                    print(lines)
                    refile.write(lines)
                    refile.write('\n')
                else:
                    # if self.checklable is not None:
                    #     if i[0].split("|")[0] == "false":
                    #         lablestr = '{} 标签： {}'.format(self.sessonids[index],
                    #                                       json.dumps(lables[self.sessonids[index]], ensure_ascii=False))
                    #         # logger.info(lablestr)
                    #         print(lablestr)
                    #         refile.write(lablestr)
                    #         refile.write("\n")
                    #         index = index + 1
                    if self.pushdeppon:
                        if i[0].split("|")[0] == "false":
                            recallinfo = '{} 推送信息 {}'.format(self.sessonids[index],
                                                             json.dumps(
                                                                 callinfo[self.sessonids[index].split("&")[1].strip()],
                                                                 ensure_ascii=False))
                            # logger.info(lablestr)
                            print(recallinfo)
                            refile.write(recallinfo)
                            refile.write("\n")
                            index = index + 1
                    # print("i[0]: ",i[0])
                    if i[0].split("|")[0].lower() == "false":
                        # print(recallinfo)
                        recallinfo = 'sessionid: {}'.format(self.sessonids[index])
                        print(recallinfo)
                        refile.write(recallinfo)
                        refile.write("\n")
                        index = index + 1
                    count_chinese = dialoguetxt.count_chinese(i[0])
                    # 汉字占两个显示所以需要*2
                    if count_chinese > 10:
                        lines = '{:20}{:30}{:30}{:20}{:20}{:20}'.format(i[0] + 10 * "-", i[1],
                                                              i[3], i[4],i[5],i[6])
                    else:
                        lines = '{:20}{:30}{:30}{:20}{:20}{:20}'.format(i[0] + (20 - dialoguetxt.count_chinese(i[0]) * 2) * "-",
                                                              i[1],
                                                              i[3], i[4],i[5],i[6])
                    print(lines)
                    refile.write(lines)
                    refile.write('\n')

    def sessionslabels(self, endtime, starttime, sessonids, checklable):
        time.sleep(30)  # 等待30s保证日期都已入库es
        lables = {}
        lablecontent = {}
        # kibana=acquirekibana(query,starttime,endtime)
        # kibana = acquirekibana(self.env)

        # labeldict = (starttime, endtime, self.pid)
        labeldict = self.getlabel(starttime, endtime, self.pid)
        logger.info("sessionslabels 处理sessonids: {}".format(sessonids))
        logger.info("sessionslabels 处理es内容：{}".format(json.dumps(labeldict, ensure_ascii=False)))
        for sessonid in sessonids:
            if labeldict.keys().__contains__(sessonid):
                pass
            else:
                time.sleep(5)
                labeldict = self.getlabel(starttime, endtime, self.pid)
        for sessionid in sessonids:
            # for k, v in labeldict.items():
            if sessionid in labeldict.keys():
                for label in checklable.keys():
                    # originallabel = json.loads(labeldict.get(sessionid))
                    originallabel = labeldict.get(sessionid)
                    if label in originallabel.keys():
                        lablecontent[checklable[label]] = originallabel[label]
                    else:
                        lablecontent[checklable[label]] = "此标签不存在"

                lables[sessionid] = copy.deepcopy(lablecontent)
                lablecontent.clear()
            else:
                lables[sessionid] = "此session未查询到标签内容"
        logger.info("sessionslabels 处理后的labels: {}".format(json.dumps(lables, ensure_ascii=False)))
        return lables

    def parselog(self, log):
        hits = log["responses"][0]["hits"]['hits']
        temp = {}
        for item in hits:
            sessionId = item["_source"]["sessionId"]
            offset = item["_source"]["offset"]
            message = item["_source"]["message"]
            if sessionId in temp.keys():
                message_logtime = []
                message_logtime.append(message)
                message_logtime.append(offset)
                temp[sessionId].append(copy.deepcopy(message_logtime))
                message_logtime.clear()
            else:
                temp[sessionId] = []
                message_logtime = []
                message_logtime.append(message)
                message_logtime.append(offset)
                temp[sessionId].append(copy.deepcopy(message_logtime))
                message_logtime.clear()
        # 排序拿出对话中最后一条标签内容
        for k, v in temp.items():
            v.sort(key=lambda x: x[1])
        # print(json.dumps(temp))
        # 截取标签值
        for k, v in temp.items():
            logger.info('处理前id {},message: {}'.format(k, v))
            last_message = v[-1][0]
            input_origin = json.loads(json.loads(last_message)["message"])["input_origin"]
            logger.info("input_origin: {}".format(json.dumps(input_origin, ensure_ascii=False)))
            reqstr = input_origin.split("req:")[1]
            callInfo = json.loads(json.loads(reqstr)["callInfo"])
            logger.info("req is : {}".format(json.dumps(callInfo, ensure_ascii=False)))
            if callInfo["fsReqInfo"]["command"] == "2":
                temp[k] = callInfo
            else:
                temp[k] = "此sessionid没有 hangup"
        logger.info("es处理后数据： {}".format(json.dumps(temp, ensure_ascii=False)))
        return temp

    # def getlabel(self, gte, lte, pid):
    #     """
    #
    #     :param gte: 开始时间
    #     :param lte: 结束时间
    #     :param pid: productid
    #     :return:
    #     """
    #     kibana = acquirekibana(self.env)
    #     query = [
    #         # {"module": "dm-engine", "productId": pid, "eventName": "contextAttrs", "operator": "是"}
    #         {"module": "dataclean-message", "productId": pid,
    #          "eventName": "http://smart-provider-boot.his.svc.cluster.local:9090/provider/api/v1/sendCallInfo",
    #          "operator": "是"}
    #     ]
    #     re = kibana.getlog(query, gte, lte)
    #     if re.status_code == 200:
    #         try:
    #             return self.parselog(re.json())
    #         except:
    #             time.sleep(15)
    #             re = kibana.getlog(query, gte, lte)
    #             if re.status_code == 200:
    #                 return self.parselog(re.json())
    #             else:
    #                 logger.info("es 无数据")
    #                 return {}
    #     else:
    #         logger.info("es 无数据")
    #         return {}

    def getpushdeppon(self, gte, lte):
        """

        :param gte: 开始时间
        :param lte: 结束时间
        :param pid: productid
        :return:
        """
        kibana = acquirekibana(self.env)
        query = [
            # {"module": "dm-engine", "productId": pid, "eventName": "contextAttrs", "operator": "是"}
            {"module": "smart-dm-inter-boot", "operator": "是"},
            {"eventName": ["pushDepponCallInfo", "pushCallInfo req is"], "operator": "属于"}
        ]
        re = kibana.getlog(query, gte, lte)
        if re.status_code != 200:
            re = kibana.getlog(query, gte, lte)
        return re

    def pushDepponCallInfo(self, endtime, starttime):
        """
        获取德邦话单推送信息
        :param endtime:
        :param starttime:
        :return:
        """
        # time.sleep(30)
        re = self.getpushdeppon(starttime, endtime)
        session_recordid = {}
        recordid_callinfo = {}
        session_callinfo = {}
        hits = re.json()["responses"][0]["hits"]["hits"]
        # sorted(hits,)
        hits.sort(key=lambda x: x["_source"]["offset"])
        for hit in hits:
            if hit["_source"]["eventName"] == "pushCallInfo req is":
                sessonid = hit["_source"]["raw"].split(",")[6].split("=")[1].strip()
                print("sessionid is: {}".format(sessonid))
                recordid = hit["_source"]["recordId"]
                if session_recordid.get(sessonid) is None:
                    session_recordid[sessonid] = []
                session_recordid[sessonid].append(recordid)
            # session_recordid[sessonid] = recordid
        print("session_recordid init is  {}".format(session_recordid))
        for hit in hits:
            if hit["_source"]["eventName"] == "pushDepponCallInfo":
                pushinfo = hit["_source"]["message__input_origin"].split("req:")[1].strip()
                # print("sessionid is: {}".format(sessonid))
                recordid = hit["_source"]["recordId"]
                recordid_callinfo[recordid] = pushinfo
        print("recordid_callinfo is {}".format(recordid_callinfo))
        for k, v in session_recordid.items():
            for recordid in v:
                if recordid_callinfo.get(recordid) is not None:
                    session_callinfo[k] = recordid_callinfo[recordid]
            # session_callinfo[k] = recordid_callinfo[v]
        print("session_callinfo is {}".format(session_callinfo))
        return session_callinfo


if __name__ == '__main__':
    # ['下班时间下单', '查件', '查询网点', '价格咨询', 'ivr', '下单']
    # start_time = time.perf_counter()
    # phone = '1026'
    # mobilephone = '18513583960'
    # # env = 'test'
    # env = 'alpha'
    # casetxt = r"ba/ivr"
    # # casetxt = r"ba/ivr"
    # # casetxt = r"ba/查件"
    # dm = dialoguetxt()
    # endtime = time.perf_counter()
    # print('time cost {}'.format(endtime - start_time))
    pass

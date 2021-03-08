# -*- coding:utf-8 -*-
import requests
import time
import json
import copy
from base.log import logger


class acquirekibana():
    index = {"alpha": "log-his-alpha-tracer-*", "beta": "log-his-beta-tracer-*", "prod": "log-his-prod-tracer-*"}
    url = {
        "alpha": "http://log.talkinggenie.com:5601/elasticsearch/_msearch?rest_total_hits_as_int=true&ignore_throttled=true",
        "beta": "http://log.talkinggenie.com:5601/elasticsearch/_msearch?rest_total_hits_as_int=true&ignore_throttled=true",
        "test": "http://log-test.talkinggenie.com:5601/elasticsearch/_msearch?rest_total_hits_as_int=true&ignore_throttled=true",
        "prod": "http://log.talkinggenie.com:5601/elasticsearch/_msearch?rest_total_hits_as_int=true&ignore_throttled=true"

    }
    header = {
        "prod": {
            "Host": "log.talkinggenie.com:5601",
            "Proxy-Connection": "keep-alive",
            "Accept": "application/json, text/plain, */*",
            "Origin": "http://log.talkinggenie.com:5601",
            "kbn-version": "6.7.2",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
            "content-type": "application/x-ndjson",
            "Referer": "http://log.talkinggenie.com:5601/app/kibana",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9"
        },
        "alpha": {
            "Host": "log.talkinggenie.com:5601",
            "Proxy-Connection": "keep-alive",
            "Accept": "application/json, text/plain, */*",
            "Origin": "http://log.talkinggenie.com:5601",
            "kbn-version": "6.7.2",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
            "content-type": "application/x-ndjson",
            "Referer": "http://log.talkinggenie.com:5601/app/kibana",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9"
        },
        "beta": {
            "Host": "log.talkinggenie.com:5601",
            "Proxy-Connection": "keep-alive",
            "Accept": "application/json, text/plain, */*",
            "Origin": "http://log.talkinggenie.com:5601",
            "kbn-version": "6.7.2",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
            "content-type": "application/x-ndjson",
            "Referer": "http://log.talkinggenie.com:5601/app/kibana",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9"
        },
        "test": {
            "Host": "log-test.talkinggenie.com:5601",
            "Proxy-Connection": "keep-alive",
            "Accept": "application/json, text/plain, */*",
            "Origin": "http://log-test.talkinggenie.com:5601",
            "kbn-version": "6.7.2",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
            "content-type": "application/x-ndjson",
            "Referer": "http://log-test.talkinggenie.com:5601/app/kibana",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9"
        }
    }

    def __init__(self, env):
        self.env = env

    def getlog(self, query, gte, lte):
        """
        :param query:
        :param gte:开始时间
        :param lte: 结束时间
        :return: 返回日志查询的结果
        """
        url = self.url[self.env]
        index = self.index[self.env]
        headers = self.header[self.env]
        index = {"index": index, "ignore_unavailable": True, "preference": int(time.time() * 1000)}
        query = acquirekibana.get_playload(query, gte, lte)
        data = json.dumps(index, ensure_ascii=False) + "\n" + json.dumps(query, ensure_ascii=False) + "\n"
        logger.info("es 查询url: {}".format(url))
        logger.info("es 查询header: {}".format(headers))
        logger.info("es查询条件为： {}".format(data))
        re = requests.post(url=url, headers=headers, data=data.encode("utf-8"))
        logger.info("es查询结果为： {}".format(re.text))
        return re

    @staticmethod
    def get_playload(query, gte, lte):
        """
        :param query:
        :param gte:
        :param lte:
        :return:
        """
        playload = {
            "version": True,
            "timeout": "30000ms",
            "size": 5000,
            "sort": "_doc",
            # "sort": [{"logTime": {"order": "asc", "unmapped_type": "boolean"}}],
            "query": {
                "bool": {
                    "must": [
                        {
                            "match_all": {
                            }
                        },
                        {
                            "range": {
                                "logTime": {
                                    "gte": gte,
                                    "lte": lte,
                                    "format": "epoch_millis"
                                }
                            }
                        }
                    ],
                    "filter": [
                    ],
                    "should": [
                    ],
                    "must_not": [
                    ]
                }
            }
        }

        querboolmust = playload["query"]["bool"]["must"]
        querboolmust_not = playload["query"]["bool"]["must_not"]
        # for item in querboolmust:
        #         #     if item.get("range") is not None:
        #         #         item["range"]["logTime"]["gte"] = start_timestamp
        #         #         item["range"]["logTime"]["lte"] = over_timestamp
        match_phrase = {}
        for item in query:
            # 解析 operator： "是"
            if item["operator"] == "是":
                for k, v in item.items():
                    if k == "operator":
                        pass
                    else:
                        match_phrasedict = {}
                        querydict = {}
                        querydict["query"] = v
                        match_phrasedict[k] = querydict
                        match_phrase["match_phrase"] = copy.deepcopy(match_phrasedict)
                        querboolmust.append(copy.deepcopy(match_phrase))
                        match_phrasedict.clear()
            # 解析 operator： "不是"
            elif item["operator"] == "不是":
                for k, v in item.items():
                    if k == "operator":
                        pass
                    else:
                        match_phrasedict = {}
                        querydict = {}
                        querydict["query"] = v
                        match_phrasedict[k] = querydict
                        match_phrase["match_phrase"] = copy.deepcopy(match_phrasedict)
                        querboolmust_not.append(copy.deepcopy(match_phrase))
                        match_phrasedict.clear()
            # 解析 operator： "属于"
            elif item["operator"] == "属于":
                for k, v in item.items():
                    if k == "operator":
                        pass
                    else:
                        booldict = {}
                        booldict["minimum_should_match"] = 1
                        booldict["should"] = []
                        match_phrasedict = {}
                        filterdict = {}
                        for conditon in v:
                            filterdict[k] = conditon
                            match_phrasedict["match_phrase"] = copy.deepcopy(filterdict)
                            booldict["should"].append(copy.deepcopy(match_phrasedict))
                        # querydict["query"] = v
                        # # ['k']['query']=v
                        # match_phrasedict[k] = querydict
                        # match_phrase["match_phrase"] = deepcopy(match_phrasedict)
                        querboolmust.append({"bool": booldict})
                        # match_phrase.clear()
                        match_phrasedict.clear()
            # 解析 operator： "不属于"
            elif item["operator"] == "不属于":
                for k, v in item.items():
                    if k == "operator":
                        pass
                    else:
                        booldict = {}
                        booldict["minimum_should_match"] = 1
                        booldict["should"] = []
                        match_phrasedict = {}
                        filterdict = {}
                        for conditon in v:
                            filterdict[k] = conditon
                            match_phrasedict["match_phrase"] = copy.deepcopy(filterdict)
                            booldict["should"].append(copy.deepcopy(match_phrasedict))
                        querboolmust_not.append({"bool": booldict})
                        match_phrasedict.clear()
            # 解析 operator： "存在"
            elif item["operator"] == "存在":
                for k, v in item.items():
                    if k == "operator":
                        pass
                    else:
                        existsdict = {}
                        filterdict = {}
                        filterdict["field"] = k
                        existsdict["exists"] = copy.deepcopy(filterdict)
                        querboolmust.append(copy.deepcopy(existsdict))
            # 解析 operator： "不存在"
            elif item["operator"] == "不存在":
                for k, v in item.items():
                    if k == "operator":
                        pass
                    else:
                        existsdict = {}
                        filterdict = {}
                        filterdict["field"] = k
                        existsdict["exists"] = copy.deepcopy(filterdict)
                        querboolmust_not.append(copy.deepcopy(existsdict))
        logger.info(json.dumps(playload, ensure_ascii=False))
        return playload


if __name__ == "__main__":
    gte = ""
    lte = ""
    # getlog(gte,lte)
    # getlabel()
    query = [
        {"module": "dm-engine", "productId": "id", "eventName": "contextAttrs", "operator": "是"}
    ]
    acquirekibana.get_playload(query, gte, lte)

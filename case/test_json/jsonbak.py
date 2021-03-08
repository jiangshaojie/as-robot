# -*- coding: utf-8 -*-
from case.test_json.dialogtxt_json import exceloperate
from case.test_json.dialogtxt_json import readfileconf
from case.test_json.dialogtxt_json import readyaml
import pytest
from case.test_json.dialogtxt_json import postservice
import datetime


def getcase(filename):
    """根据文件名，获取用例"""
    filepropertys = readfileconf(filename)
    re = []
    for fileproperty in filepropertys:
        if fileproperty["run"] == True:
            if fileproperty.get("time") is not None:
                runtime = fileproperty.get("time")
                timekeeper = datetime.datetime.now().strftime("%H:%M:%S")
                if runtime[0] < timekeeper < runtime[1]:
                    a = exceloperate(fileproperty["env"], fileproperty["phone"], fileproperty["file"],
                                     fileproperty["sheetnames"],fileproperty.get("randphone"))
                    re.extend(a.getcase())
            else:
                a = exceloperate(fileproperty["env"], fileproperty["phone"], fileproperty["file"],
                                 fileproperty["sheetnames"],fileproperty.get("randphone"))
                re.extend(a.getcase())
    return re


def getquerys(filename):
    """根据文件名，获取querys"""
    fileproperty = readfileconf(filename)
    a = exceloperate(fileproperty["env"], fileproperty["phone"], fileproperty["file"], fileproperty["sheetnames"])
    return a.getquerys()


post = postservice()


def querycase(cases):
    # post = postservice()
    # for case in cases:
    flag = True
    post.postall(cases)
    for case in cases:
        if case["answerexpcet"] is not None:
            if case["answerexpcet"] == case["titleclown"]:
                case["actioncompare"] = "pass"
            else:
                case["actioncompare"] = "fail"
        if case["topiccodeexpect"] is not None:
            if str(case["topiccodeexpect"]) == case["topiccode"]:
                case["topiccompare"] = "pass"
            else:
                case["topiccompare"] = "fail"
        if case.get("actioncompare") == "fail" or case.get("topiccompare") == "fail":
            case["casecompare"] = "fail"
        elif case.get("actioncompare") == "pass" and case.get("topiccompare") == "pass":
            case["casecompare"] = "pass"
        # for case in cases:
        if case.get("casecompare") == "fail":
            flag = False
    return cases, flag


class Test_json():
    re = []

    def setup_class(self):
        fileconf = readyaml()
        # filepropertys=readfileconf()
        for fileproperty in fileconf["filenames"]:
            if fileproperty["run"] == True:
                if fileproperty.get("time") is not None:
                    runtime = fileproperty.get("time")
                    timekeeper = datetime.datetime.now().strftime("%H:%M:%S")
                    if runtime[0] < timekeeper < runtime[1]:
                        fileobject = exceloperate(fileproperty["env"], fileproperty["phone"], fileproperty["file"],
                                                  fileproperty["sheetnames"])
                        fileobject.before_execute()
                else:
                    fileobject = exceloperate(fileproperty["env"], fileproperty["phone"], fileproperty["file"],
                                              fileproperty["sheetnames"])
                    fileobject.before_execute()
        print("setup_class 执行完毕")

    @pytest.mark.parametrize("cases", getcase("biguiyuan.xlsx"))
    def test_biguiyuan(self, cases):
        queryresult = querycase(cases)
        print("执行用例 ",cases[0]["sheetname"] , [x["param"]["query"] for x in cases])
        try:
            assert queryresult[1]
        finally:
            self.re.append(queryresult[0])

    @pytest.mark.parametrize("cases", getcase("debangba_alpha.xlsx"))
    def test_debang_alpha(self, cases):
        queryresult = querycase(cases)
        print("执行用例 ",cases[0]["sheetname"] , [x["param"]["query"] for x in cases])
        try:
            assert queryresult[1]
        finally:
            self.re.append(queryresult[0])

    @pytest.mark.parametrize("cases", getcase("debangba_test.xlsx"))
    def test_debang_test(self, cases):
        queryresult = querycase(cases)
        print("执行用例 ",cases[0]["sheetname"] , [x["param"]["query"] for x in cases])
        try:
            assert queryresult[1]
        finally:
            self.re.append(queryresult[0])

    def teardown_class(self):
        """
        对 有结果存在 re中的文件进行结果回填。
        :return:
        """
        fileconf = readyaml()
        file_re = {}
        # 文件名、casegroup为 k,v 的方式存贮
        for fileproperty in fileconf["filenames"]:
            if fileproperty["run"] == True:
                file_re[fileproperty["file"]] = []
        while len(self.re) > 0:
            casegroup = self.re.pop(0)
            file_re[casegroup[0]["filename"]].append(casegroup)
        for fileproperty in fileconf["filenames"]:
            if fileproperty["run"] == True and len(file_re[fileproperty["file"]]) > 0:
                fileobject = exceloperate(fileproperty["env"], fileproperty["phone"], fileproperty["file"],
                                          fileproperty["sheetnames"])
                querys = fileobject.getquerys()
                if len(querys) > 0:
                    queryintent = postservice()
                    queryintent.postintent(querys)
                fileobject.after_execute(file_re[fileproperty["file"]], querys)

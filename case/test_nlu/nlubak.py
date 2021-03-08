# -*- coding: utf-8 -*-
import pytest
from case.test_nlu.nlutest import NluTest
from copy import deepcopy
import sys, os
import time
from os import path

d = path.dirname(__file__)
parent_path1 = os.path.dirname(d)
parent_path2 = os.path.dirname(parent_path1)


def getcases(filename):
    rootdir = sys.path[1].replace("\\", "/")
    caseconfs = NluTest.readyaml()
    cases = []
    for caseconf in caseconfs["filenames"]:
        if caseconf["file"] == filename:
            if caseconf["run"] == True:
                file = parent_path2 + "/data/test_nlu/" + caseconf["file"]
                sheetname = caseconf["sheetnames"]
                print(file, sheetname)
                a = NluTest(file, sheetname)
                case = a.main()
                for item in case:
                    item["env"] = caseconf["env"]
                cases.extend(case)
                case.clear()
                print("执行完毕")
    return cases


def before_execute():
    print("before_execute")
    caseconfs = NluTest.readyaml()
    print("caseconfs", caseconfs)
    rootdir = sys.path[1].replace("\\", "/")
    for conf in caseconfs["filenames"]:
        if conf["run"] == True:
            file = parent_path2 + "/data/test_nlu/" + conf["file"]
            sheetname = conf["sheetnames"]
            nlu = NluTest(file, sheetname)
            nlu.move_reintent()
            nlu.move_precision_rate()
            nlu.reset()
            nlu.save()


def after_execute(re):
    filesname = {}
    for item in re:
        if filesname.get(item["filename"]) is None:
            filesname[item["filename"]] = set()
            filesname[item["filename"]].add(item["sheetname"])
        else:
            filesname[item["filename"]].add(item["sheetname"])
    filesobject = {}
    for k, v in filesname.items():
        filesobject[k] = NluTest(k, v)
    for r in re:
        filesobject[r["filename"]].parsere(r)
    for k, v in filesobject.items():
        v.casecompare()
        v.save()


def runnlu(cases):
    pid = cases["pid"]
    queryintent = cases["queryintent"].split(",")
    queryintentlist = [intent.strip() for intent in queryintent]
    expectintentlist = [intent.strip() for intent in cases["expectintents"].split(",")]
    print("查询语料： {}".format(cases["query"]))
    r = NluTest.nlufusionquery(pid, cases["query"], queryintentlist, cases["env"])
    cases["reintent"] = r[0]
    cases["reslots"] = r[1]
    # expectintents=queryexpectintent
    flag = False
    for intent in r[0].split(","):
        if expectintentlist.__contains__(intent):
            cases["testre_intent"] = True
            # pass
        else:
            # flag = False
            cases["testre_intent"] = False
    if cases["expectslots"] is None:
        cases["testre_slots"] = None
        pass
    else:
        testre_slots = False
        try:
            for intent, slots in eval(cases["expectslots"]).items():
                reslots = r[1][intent]
                for slot in slots:
                    for reslot in reslots:
                        if reslot["slot"] == slot["slot"] and reslot["value"] == slot["value"]:
                            testre_slots = True
                        else:
                            testre_slots = False
            cases["testre_slots"] = testre_slots
        except:
            testre_slots = False
            cases["testre_slots"] = testre_slots
    if cases["testre_intent"] == True and cases["testre_slots"] == True:
        cases["testre"] = True
        flag = True
    elif cases["testre_intent"] == True and cases["testre_slots"] == None:
        cases["testre"] = True
        flag = True
    else:
        cases["testre"] = False
        flag = False
    return flag, cases


# @pytest.fixture(scope="class", params=getcases())
# def cases(request):
#     return request.param


class Test_nlu():
    re = []

    def setup_class(self):
        print("start")
        before_execute()

    @pytest.mark.parametrize("cases", getcases("debang.xlsx"))
    def test_debang(self, cases):
        re = runnlu(cases)
        try:
            assert re[0]
        finally:
            self.re.append(deepcopy(re[1]))

    @pytest.mark.parametrize("cases", getcases("ytoqcj.xlsx"))
    def test_yto(self, cases):
        re = runnlu(cases)
        try:
            assert re[0]
        finally:
            self.re.append(deepcopy(re[1]))

    def teardown_class(self):
        # print("teardown class哈哈哈")
        # print(self.re)
        after_execute(self.re)

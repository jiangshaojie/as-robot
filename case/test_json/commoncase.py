# -*- coding: utf-8 -*-
from case.test_json.dialogtest import runcase
from case.test_json.dialogtest import runcase_shell
from case.test_json.case_debang import update_time_inpart
from case.test_json.case_debang import CourierTime

def run():
    case = "sf_quanchangjing.xlsx"
    sheetnames = ["禁止下单地址"]
    runcase(case, sheetnames=sheetnames, threadnum=5)

def run_private():
    url = "http://47.97.158.11:19103/dataclean/message/yto/messages/v2"
    casename = r"C:\code\platform-regression-python\data\test_json\sf_quanchangjing.xlsx"
    sheetname = None
    runcase_shell(casename=casename, url=url, sheetnames=sheetname, threadnum=1)


if __name__ == '__main__':
    # run()
    debang()
    # debang()
    # run_private()

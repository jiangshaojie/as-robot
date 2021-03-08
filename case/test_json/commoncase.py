# -*- coding: utf-8 -*-
from case.test_json.dialogtest import runcase
from case.test_json.dialogtest import runcase_shell
from case.test_json.case_debang import update_time_inpart
from case.test_json.case_debang import CourierTime

def run():
    case = "sf_quanchangjing.xlsx"
    # case="y_test.xlsx"
    # case = "sf_waihu.xlsx"
    # sheetnames = None
    # sheetnames = ["高峰管控1"]
    # sheetnames = ["拒收"]
    # sheetnames = ["投诉"]
    # sheetnames = ["修改收方信息"]
    # sheetnames = ["退回"]
    # sheetnames = ["价格咨询"]
    sheetnames = ["禁止下单地址"]
    # sheetnames = ["查单"]
    # sheetnames = ["催单"]
    # sheetnames = ["特殊查单","ivr"]
    # runcase(case, sheetnames=sheetnames,threadnum=2,check_topic_type="transernum_servicetype")
    runcase(case, sheetnames=sheetnames, threadnum=5)
    # print(os.path.exists(case))


def debang():
    case = "debangba_test.xlsx"
    # sheetnames = ["查件", "咨询网点", "下班时间下单", "下班时间ivr", "价格咨询","查询网点","查件alpha"]
    # sheetnames=None
    # runcase(case, sheetnames=sheetnames, threadnum=10)
    # case = "debangba_alpha.xlsx"
    # sheetnames = ["查件", "查询网点"]
    # runcase(case, sheetnames=sheetnames, threadnum=10)
    # sheetnames = ["test"]
    # sheetnames = ["截单测试"]
    # update_time_inpart(courier_time.OFFICE_HOUR)
    # sheetnames = ["下单"]
    # update_time_inpart(CourierTime.CLOSING_TIME)
    sheetnames = ["禁止下单地址"]
    # sheetnames = ["查询网点"]
    # sheetnames = ["下单", "ivr"]
    runcase(case, sheetnames=sheetnames, threadnum=5)


def run_private():
    url = "http://47.97.158.11:19103/dataclean/message/yto/messages/v2"
    # url = "http://nlu-test.talkinggenie.com/dataclean/message/yto/messages/v2"
    # url = "http://debugcheck-beta.talkinggenie.com/dataclean/message/yto/messages/v2"
    casename = r"C:\code\platform-regression-python\data\test_json\sf_quanchangjing.xlsx"
    # sheetname = ["快件损坏"]
    sheetname = None
    runcase_shell(casename=casename, url=url, sheetnames=sheetname, threadnum=1)


if __name__ == '__main__':
    # run()
    debang()
    # debang()
    # run_private()

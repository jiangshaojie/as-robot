# -*- coding: utf-8 -*-
from case.test_nlu.nlutest import runcase


def run_signle():
    # filename = "taicangnuoche.xlsx"
    # filename = "sf_quanchangjing_nlu.xlsx"
    # filename = "guanwu.xlsx"
    filename = "test.xlsx"
    filename = "peilianyitu.xlsx"
    # filename = "debangwaihu_nlu.xlsx"
    # filename = "debang.xlsx"
    # filename = "yunpinlv_nlu.xlsx"
    sheetnames = ["Sheet2"]
    # sheetnames = ["test"]
    # sheetnames = None
    runcase(filename, threadnum=1, sheetnames=sheetnames)


def run_all():
    filenames = ["sf_quanchangjing_nlu.xlsx", "debang.xlsx"]
    for filename in filenames:
        runcase(filename, threadnum=3)


if __name__ == '__main__':
    # run_all()
    run_signle()

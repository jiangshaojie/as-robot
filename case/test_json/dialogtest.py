# -*- coding: utf-8 -*-
from case.test_json.dialogtxt import dialogtxt
import yaml
import sys
import datetime
from base.readpath import getpath
import os
from case.test_json.readconfig import ReadConfig
import json
from base.log import logger


def readyaml(casename):
    """
     根据casename 返回用例场景配置信息。
    :param casename:
    :return:
    """
    # print(sys.path)
    rootdir = getpath()
    file = rootdir + "/data/test_json/test_j.yaml"
    with open(file, "r", encoding="utf-8") as conf:
        cases = yaml.load_all(conf.read(), Loader=yaml.FullLoader)
        for case in cases:
            if case.get(casename) is not None:
                for file in case[casename]:
                    file["file"] = rootdir + "/data/test_json/" + file["file"]
                return case


def getcase(casename):
    """根据文件名，获取用例"""
    try:
        filepropertys = readyaml(casename).get(casename)
        re = {}
        timekeeper = datetime.datetime.now().strftime("%H:%M:%S")
        for fileproperty in filepropertys:
            runtime = fileproperty.get("time")
            run_filter_time = True
            try:
                if timekeeper < runtime[0] or timekeeper > runtime[1]:
                    run_filter_time = False
            except Exception as e:
                print("没有配置运行时间，默认运行")
            if fileproperty["run"] == True and run_filter_time:
                if fileproperty["file"] in re:
                    if fileproperty["env"] in re[fileproperty["file"]]:
                        if fileproperty["phone"] in re[fileproperty["file"]][fileproperty["env"]]:
                            re[fileproperty["file"]][fileproperty["env"]][fileproperty["phone"]].extend(
                                fileproperty["sheetnames"])
                        else:
                            re[fileproperty["file"]][fileproperty["env"]][fileproperty["phone"]] = fileproperty[
                                "sheetnames"]
                    else:
                        re[fileproperty["file"]][fileproperty["env"]] = {}
                        re[fileproperty["file"]][fileproperty["env"]][fileproperty["phone"]] = fileproperty[
                            "sheetnames"]
                else:
                    re[fileproperty["file"]] = {}
                    re[fileproperty["file"]][fileproperty["env"]] = {}
                    re[fileproperty["file"]][fileproperty["env"]][fileproperty["phone"]] = fileproperty[
                        "sheetnames"]
    except:
        re = {}

    return re


def getcase_excelconfig(filename, sheetnames):
    """根据excel配置获取用例,若传入sheetname数组，则只读取传入的sheet配置"""
    config = ReadConfig(filename)
    config_bot = config.readbot()
    logger.info("收集到可执行表： {}".format(config_bot))
    if sheetnames != None:
        config_bot_new = {}
        excute_excel = []
        for sheetname in sheetnames:
            for env, init_sheetnames in config_bot.items():
                if init_sheetnames.__contains__(sheetname):
                    if config_bot_new.get(env) == None:
                        config_bot_new[env] = []
                    config_bot_new[env].append(sheetname)
                    excute_excel.append(sheetname)
        # excute_excel=[]
        if len(excute_excel) != len(sheetnames):
            loseexcel = []
            for sheetname in sheetnames:
                if excute_excel.__contains__(sheetname) == False:
                    loseexcel.append(sheetname)
            print(Exception("{} 表未找到或者run参数为False".format(loseexcel.__str__())))
        config_bot = config_bot_new
    logger.info("测试用例执行sheet为： {}".format(json.dumps(config_bot, ensure_ascii=False)))
    return config_bot


# randphone=True
def runcase(casename, randphone=False, threadnum=None, sheetnames=None,check_topic_type=None):
    files = getcase(casename)
    print(files.__str__())
    # fileslist = files["filenames"]
    if len(files) > 0:
        for file, fileproperty in files.items():
            for env, phone_sheetnames in fileproperty.items():
                for phone, sheetnames in phone_sheetnames.items():
                    print(phone, sheetnames)
                    dialog = dialogtxt(file, env, phone, sheetnames, randphone, threadnum,check_topic_type=check_topic_type)
                    dialog.main()
    elif os.path.exists(casename):
        print("自定义路径文件存在")
        config_bot = getcase_excelconfig(casename, sheetnames)
        for env, sheetnames in config_bot.items():
            dialog = dialogtxt(excelpath=casename, env=env, phone="1025", sheetnames=sheetnames, randphone=randphone,
                               threadnum=threadnum,check_topic_type=check_topic_type)
            dialog.main()
    else:
        rootdir = getpath()
        file = rootdir + "/data/test_json/" + casename
        print(file)
        if os.path.exists(file):
            print("文件存在")
            config_bot = getcase_excelconfig(file, sheetnames)
            for env, sheetnames in config_bot.items():
                dialog = dialogtxt(excelpath=file, env=env, phone="1025", sheetnames=sheetnames, randphone=randphone,
                                   threadnum=threadnum,check_topic_type=check_topic_type)
                dialog.main()
        else:
            print("文件不存在： ",file)

def run_data(casename, randphone=False, threadnum=None, sheetnames=None,check_topic_type=None):
    files = getcase(casename)
    print(files.__str__())
    # fileslist = files["filenames"]
    if len(files) > 0:
        for file, fileproperty in files.items():
            for env, phone_sheetnames in fileproperty.items():
                for phone, sheetnames in phone_sheetnames.items():
                    print(phone, sheetnames)
                    dialog = dialogtxt(file, env, phone, sheetnames, randphone, threadnum,check_topic_type=check_topic_type)
                    dialog.main_data()
    elif os.path.exists(casename):
        print("自定义路径文件存在")
        config_bot = getcase_excelconfig(casename, sheetnames)
        for env, sheetnames in config_bot.items():
            dialog = dialogtxt(excelpath=casename, env=env, phone="1025", sheetnames=sheetnames, randphone=randphone,
                               threadnum=threadnum,check_topic_type=check_topic_type)
            dialog.main_data()
    else:
        rootdir = getpath()
        file = rootdir + "/data/test_json/" + casename
        print(file)
        if os.path.exists(file):
            print("文件存在")
            config_bot = getcase_excelconfig(file, sheetnames)
            for env, sheetnames in config_bot.items():
                dialog = dialogtxt(excelpath=file, env=env, phone="1025", sheetnames=sheetnames, randphone=randphone,
                                   threadnum=threadnum,check_topic_type=check_topic_type)
                dialog.main_data()
        else:
            print("文件不存在： ",file)


def runcase_shell(casename, url, dmurl=None, randphone=False, threadnum=None,sheetnames=None):
    if os.path.exists(casename):
        print("文件存在")
    config_bot = getcase_excelconfig(casename,sheetnames)
    for env, sheetnames in config_bot.items():
        dialog = dialogtxt(excelpath=casename, env=env, phone="1025", sheetnames=sheetnames, randphone=randphone,
                           threadnum=threadnum)
        if url != "":
            dialog.url = url
        if dmurl != "":
            dialog.dmruntimeurl = dmurl
        dialog.main()


if __name__ == "__main__":
    case = "yunpinlvtest.xlsx"
    runcase(case, threadnum=1)

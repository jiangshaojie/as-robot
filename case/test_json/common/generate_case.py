# -*- coding: utf-8 -*-
from copy import copy


def generate():
    citys = "北京市大兴区;北京市昌平区;呼伦贝尔鄂温克族自治旗;呼伦贝尔                    陈巴尔虎旗;呼伦贝尔鄂温克族自治旗;呼伦贝尔鄂温克族自治旗;呼伦贝尔鄂温克族自治旗"
    city = """北京市大兴区
    呼伦贝尔鄂温克族自治旗
    呼伦贝尔陈巴尔虎旗
    呼伦贝尔新巴尔虎左旗
    呼伦贝尔新巴尔虎右旗
    呼伦贝尔阿荣旗
    呼伦贝尔海拉尔
    呼伦贝尔莫力达瓦达斡尔族自治旗
    呼伦贝尔扎兰屯市
    四平市公主岭市
    白城市大安市
    通化市东昌区
    通化市二道江区
    通化市通化县
    通化市辉南县
    通化市柳河县
    通化市集安市
    松原市宁江区
    松原市前郭尔罗斯蒙古族自治县
    渭南市白水县
    绥化市FULL
    黑河市爱辉区
    黑河市逊克县
    黑河市孙吴县
    黑河市北安市
    齐齐哈尔市昂昂溪区
    齐齐哈尔市拜泉县
    齐齐哈尔市富拉尔基区
    齐齐哈尔市梅里斯达斡尔族区
    齐齐哈尔市龙江县
    齐齐哈尔市讷河市
    齐齐哈尔市克山县
    齐齐哈尔市依安县
    牡丹江市林口县
    伊春市铁力市
    伊春市带岭区
    哈尔滨市五常市
    哈尔滨市松北区
    哈尔滨市呼兰区
    大庆市杜尔伯特蒙古族自治县
    大庆市肇州市
    大庆市林甸县
    双鸭山市友谊县
    佳木斯市同江市"""
    cases = ["false", "下单", "书"]
    cases_new = list()
    # for city in citys.split(";"):
    for city in city.split("\n"):
        print(city)
        case_new = copy(cases)
        case_new.append(city.strip())
        cases_new.extend(case_new)
    print(cases_new)
    with open("generate.txt", "w", encoding="utf-8") as f:
        for case in cases_new:
            f.write(case)
            f.write("\n")


if __name__ == '__main__':
    generate()

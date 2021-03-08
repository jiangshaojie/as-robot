# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome import options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import requests
import json
import redis
from urllib import parse


class SynJson(object):
    username_password = {
        "name": "蒋少杰",
        "username": "shaojie.jiang",
        "password": "101edaLK158@"
    }
    header = {
        'authority': 'alpha.talkinggenie.com',
        'accept': 'application/json, text/plain, */*',
        'username': parse.quote(username_password.get("name")),
        'authtoken': 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJzaGFvamllLmppYW5nI-iSi-WwkeadsCMxNTg2MjU4Mzg2MjYwIn0.5uHd0ef16AFC5FMm_xWICWHL1yu0hPo7P4aHPw0kx3zitmRkoSFjIlc0OPn-JZVs55rlKSo7E7I3eDaDwpZsHw',
        'sec-fetch-dest': 'empty',
        'basource': 'kf',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
        'origin': 'https://ics-admin-alpha.talkinggenie.com',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'referer': 'https://ics-admin-alpha.talkinggenie.com/dm/',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': 'cookie'
    }

    def __init__(self, botname):
        self.pool = redis.ConnectionPool(host='10.12.6.91', port=4888, password='6Qhq8BeRWE7WYOLqRjhwP233ujB1zSPR')
        self.botname = botname
        self.setheader()

    def teardown(self):
        self.pool.disconnect()

    def setheader(self):
        redisclient = redis.Redis(connection_pool=self.pool)
        cookie_auth = redisclient.get("cookie_auth")
        print("first get redis cookie_auth: {}".format(cookie_auth))
        if cookie_auth is None:
            self.writetoken()
            cookie_auth = redisclient.get("cookie_auth")
            print("second get redis cookie_auth: {}".format(cookie_auth))
        self.header["authtoken"] = json.loads(cookie_auth)["authtoken"]
        self.header["cookie"] = json.loads(cookie_auth)["cookie"]
        print("header: {}".format(json.dumps(self.header)))
        # print(json.dumps(self.header))

    def gettoken(self):
        driverpath = "C:\software\chromedriver_win32\chromedriver.exe"
        chrome_option = options.Options()
        chrome_option.add_argument('--headless')
        bowser = webdriver.Chrome(driverpath, options=chrome_option)
        bowser.implicitly_wait(10)
        bowser.get(
            "https://admin-alpha.talkinggenie.com/login/?service=https://ics-admin-alpha.talkinggenie.com/#/layout/sysper")
        element = bowser.find_element_by_xpath("/html/body/div[1]/div/div[2]/form/div[1]/label")
        print(element.text)
        username = bowser.find_element_by_xpath("/html/body/div[1]/div/div[2]/form/div[1]/div/div/input")
        password = bowser.find_element_by_xpath("/html/body/div[1]/div/div[2]/form/div[2]/div/div/input")
        username.send_keys(self.username_password.get("username"))
        password.send_keys(self.username_password.get("password"))
        # login=bowser.find_element_by_xpath("/html/body/div[1]/div/div[2]/form/div[3]/button")
        # actions=ActionChains(bowser)
        # login.click()
        # actions.click(login)
        # print("执行click")
        # password.send_keys()
        # time.sleep(5)
        password.send_keys(Keys.RETURN)
        print("执行回车")
        name2 = bowser.find_element_by_class_name("hd-name")
        print("name2")
        print(name2.tag_name)
        print(name2.text)
        p = bowser.get_screenshot_as_png()
        with open("p.png", "wb") as f:
            f.write(p)
        a = bowser.get_cookies()
        bowser.close()
        if len(a) > 0:
            for item in a:
                if item["domain"] == ".talkinggenie.com":
                    return "{}={}".format(item["name"], item["value"])
                else:
                    print("cookie 获取失败")
                    return None

    def writetoken(self):
        cookie = self.gettoken()
        if cookie is None:
            print("cookie 空值未保存redis")
        else:
            cookie_auth = {}
            cookie_auth["cookie"] = cookie
            cookie_auth["authtoken"] = cookie.split("=")[1]
            redisclient = redis.Redis(connection_pool=self.pool)
            redisclient.set("cookie_auth", json.dumps(cookie_auth))

    def getjson(self):
        url = "https://alpha.talkinggenie.com/api/v2/smart/smart/sadmin/api/v1/bot-publish/"
        reversion = self.getonlineversion(self.botname)
        bot_id = json.loads(reversion)["data"]["content"][0]["id"]
        botjson = requests.get(url=url + bot_id, headers=self.header)
        print("botjson: {}".format(botjson.text))
        with open(self.botname, "w", encoding="utf-8") as f:
            f.write(json.loads(botjson.text)["data"]["jsonDetail"])
        # return json.loads(botjson.text)["data"]["jsonDetail"]

    def getonlineversion(self, botname):
        query = {"botName": botname, "online": 1}
        url = """https://alpha.talkinggenie.com/api/v2/smart/smart/sadmin/api/v1/bot-publish?pageNo=0&pageSize=1&query=%s""" % (
            json.dumps(query))
        re = requests.get(url=url, headers=self.header)
        if re.status_code != 200:
            self.writetoken()
            self.setheader()
            re = requests.get(url=url, headers=self.header)
        print(re.text)
        print(re.status_code)
        return re.text

    def synchronsizedata(self, pid, env):
        """
        同步话术用
        :param pid: 项目pid
        :param env: 环境配置 test,beta
        :return:
        """
        url = "https://alpha.talkinggenie.com/api/v2/smart/sadmin-extend/release/v1/synchronize/data?prodId={}&targetEnv={}".format(
            pid, env)
        re = requests.get(url=url, headers=self.header)
        if re.status_code != 200:
            self.writetoken()
            self.setheader()
            re = requests.get(url=url, headers=self.header)
        print("同步话术响应结果：{}".format(re.text))
        # print(re.status_code)
        print("{}_{} 同步话术到 {} 环境 {}".format(self.botname, pid, env, re.json()["message"]))
        # return re.text


if __name__ == '__main__':
    # cookie=gettoken()
    # print(cookie)
    botname = "顺丰物流全场景机器人"
    # getonlineversion(botname)
    #
    synjson = SynJson(botname)
    # r = synjson.gettoken()
    synjson.getjson()
    # synjson.writetoken()
    # synjson.setheader()

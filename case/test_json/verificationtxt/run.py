# -*- coding: utf-8 -*-
from case.test_json.dialoguewithtxt import dialoguetxt
import click

"""
顺丰全场景 txt测试。
"""


@click.command()
@click.option('--url', '--url', default='')
@click.option('--dmurl', '--dmurl', default='')
@click.option('--filename', '--f', default='')
def run(url, dmurl, filename):
    phone = '1026'
    pid = "914012099"
    env = 'prod'
    file = filename
    lables = {"is_benren": "是否接到疑似诈骗电话", "is_shouji": "能否提供诈骗手机号", "result_phone_num": "诈骗手机号",
              "is_other": "能否提供诈骗QQ或者微信", "is_qq": "能否提供诈骗QQ号", "result_num": "诈骗QQ号",
              "is_weixin": "能否提供诈骗微信号", "num_weixin": "诈骗微信号"}
    dialogue = dialoguetxt(env, phone, pid, file, checklabel=lables)
    dialogue.url = url
    dialogue.dmurl = dmurl
    dialogue.testcase()


if __name__ == '__main__':
    # url = "http://nlu-alpha.talkinggenie.com/dataclean/message/yto/messages/v2"
    # dmurl = "http://dm-runtime-alpha.talkinggenie.com/callcenter/nlu"
    run()

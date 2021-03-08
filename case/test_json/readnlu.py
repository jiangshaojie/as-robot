# -*- coding: utf-8 -*-
import json


class ReadNlu():
    def __init__(self, file):
        self.filname = file
        self.bot = self.getbot()

    def get_intent_name(self, dialog_intent_name):
        """
        获取bot意图对应的fusion意图
        :return:
        """
        # botflow = self.bot.get("botFlows")
        # print(botflow)
        intent_value = {}
        dialog_intents = self.bot.get("dialogIntents")
        for intent in dialog_intents:
            if intent.get("dialogIntentName") == dialog_intent_name:
                intent_value["referenceNluIntents"] = intent.get("referenceNluIntents")
                intent_value["proReferenceNluIntents"] = intent.get("proReferenceNluIntents")
                return intent_value

    def getbot(self):
        """
        获取bot
        :return:
        """
        with open(self.filname, encoding="UTF-8") as f:
            bot = json.load(f)
        return bot

    def get_flow_to_flow(self):
        botflow = self.bot.get("botFlows")
        startnode=botflow[0]
        flowname=startnode.get()
if __name__ == '__main__':
    file = "芸品绿网络贷款_1595318248058.json"
    readnlu = ReadNlu(file)
    intent = readnlu.get_intent_name("确认")
    print(intent)

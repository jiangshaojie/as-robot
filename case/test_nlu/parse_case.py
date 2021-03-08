# -*- coding: utf-8 -*-
import json

with open("case", "r", encoding="utf-8") as case_file:
    cases = case_file.readlines()
    for line in cases:
        caselist = eval(line)
        print(caselist)
        with open("case_export","a",encoding="utf-8") as export_file:
            for case in caselist:
                query = case.get("query")
                expect_intents = case.get("expectintents")
                query_intent = case.get("queryintent")
                try:
                    # json.loads(expect_intents)
                    expect_intents_filter = eval(expect_intents).get("GLB").strip()
                except:
                    expect_intents_filter = expect_intents.split(":")[1].strip()
                try:
                    # json.loads(expect_intents)
                    query_intents_filter = eval(query_intent).get("GLB").strip()
                except:
                    query_intents_filter = query_intent.split(":")[1].strip()
                export_file.write(query+"|"+expect_intents_filter+"|"+query_intents_filter)
                export_file.write("\n")
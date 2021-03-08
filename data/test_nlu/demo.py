# -*- coding: utf-8 -*-
import yaml
def readyaml():
    file= "case.yaml"
    with open(file,"r",encoding="utf-8") as conf:
        b=yaml.load(conf.read(),Loader=yaml.FullLoader)
        print(b)

readyaml()


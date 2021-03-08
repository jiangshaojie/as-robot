# -*- coding: UTF-8 -*-
import os
import sys
def getpath():
    rootdir=sys.path[0].replace("\\","/").split("platform-regression-python")[0]+"platform-regression-python"
    return rootdir
if __name__=="__main__":
    getpath()
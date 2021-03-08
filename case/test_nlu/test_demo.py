# -*- coding: utf-8 -*-
import pytest
from functools import wraps
def getcase(a,b):
    print("执行getcase")


    return [a,b]
def runtime(case):
    print("runtime: "+case)

def run(f):
    @wraps(f)
    def runtest(self,cases):
        print("runtest:  "+cases)
        if cases == "a1":
            raise Exception("此函数被执行")
    return runtest

class Test_demo():
    
    def setup_class(self):
        print("开始执行setup_class")
    @pytest.mark.parametrize("cases",getcase("a1","a2"))
    @run
    def test_a(self,cases):
        print("test_a: "+cases)
    @pytest.mark.parametrize("cases",getcase("b1","b2"))
    @run
    def test_b(self,cases):
        print("test_b: "+cases)
        


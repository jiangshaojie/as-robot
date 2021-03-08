# -*- coding: utf-8 -*-
import pytest
from case.test_nlu.nlutest import NluTest
from case.test_nlu.nlutest import getcases
from case.test_nlu.nlutest import after_execute
from case.test_nlu.nlutest import runnlu
from copy import deepcopy
import sys
import os
import time
from os import path
from functools import wraps
from base.log import logger

d = path.dirname(__file__)
parent_path1 = os.path.dirname(d)
parent_path2 = os.path.dirname(parent_path1)


def run(f):
    @wraps(f)
    def nluquery(self, cases):
        re = runnlu(cases)
        print("cases is: ", str(cases))
        try:
            assert re[0]
        finally:
            self.re.append(deepcopy(re[1]))
        # return f(*args,**kwargs)

    return nluquery


class Test_nlu():
    re = []

    # def setup_class(self):
    #     print("start")
    #     before_execute()

    @pytest.mark.parametrize("cases", getcases("debang.xlsx"))
    @run
    def test_debang(self, cases):
        pass

    @pytest.mark.parametrize("cases", getcases("ytoqcj.xlsx"))
    @run
    def test_yto(self, cases):
        pass

    @pytest.mark.parametrize("cases", getcases("sf_quanchangjing_nlu.xlsx"))
    @run
    def test_sf_quanchangjing(self, cases):
        pass

    @pytest.mark.parametrize("cases", getcases("taicangnuoche.xlsx"))
    @run
    def test_taicangnuoche(self, cases):
        pass

    def teardown_class(self):
        after_execute(self.re)

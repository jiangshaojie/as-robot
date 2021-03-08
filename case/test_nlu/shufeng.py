# -*- coding: utf-8 -*-
from case.test_nlu.nlutest import runcase

filename = "sf_quanchangjing_nlu.xlsx"
# filename = "fengchao.xlsx"
runcase(filename,threadnum=3)

# -*- coding: utf-8 -*-
from case.test_json.dialogtest import runcase
randphone = True
case="debang"
runcase(case,randphone)
case="debang_repeated_calls"
runcase(case,randphone,1)
cases=["debang","sfquanchanjing"]
for case in cases:
    runcase(case)

cases=["debang_repeated_calls"]

runcase(case,randphone,1)
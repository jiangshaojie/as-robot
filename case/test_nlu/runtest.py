# -*- coding: utf-8 -*-
import pytest
file=r"C:/code/platform-regression-python/case/test_nlu/test_nlu.py::Test_nlu::test_yto"
# file= r"/case/test_nlu\test_nlu.py"

# a=['-v',file , '--html', 'report/all_auto_test_report_tester.html', '-n=auto']
a=['-v',file , '--html', 'report/all_auto_test_report_tester.html', '-n=1']
c=["-v -s test_nlu.py::Test_Class::test_yto"]
b=['-v',file , '--html', 'report/all_auto_test_report_tester.html','--tests-per-worker=1']
pytest.main(a)
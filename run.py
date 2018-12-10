import HTMLTestReportCN
import time
from Event.client import *
from xml.etree.ElementTree import ElementTree as ET
"""
动态代码获取用例
下部代码逻辑
'因使用ddt实现数据驱动'动态代码在获取用例时会出现错误
加入判断:当获取用例时出现错误时,进入以下代码逻辑
--获取用例类名下的全部方法
"""


suite = unittest.TestSuite()

doc = ET().parse(source='./config.xml')
li = doc.findall('./cases/*')

for l in li:
    classname = l.tag.split('-')[0]
    methodname = l.tag.split('-')[1]
    CASES_INFO = '''from Event.cases.{classname} import {classname}
suite.addTest({classname}("test_{methodname}"))'''.format(classname=classname, methodname=methodname)
    try:
        exec(CASES_INFO)
    except ValueError:
        ddt_cases = eval('unittest.defaultTestLoader.getTestCaseNames(%s)' % (classname))
        for ddt_c in ddt_cases:
            if ddt_c.startswith('test_' + methodname):
                exec("suite.addTest(%s('%s'))" % (classname, ddt_c))

now = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
report_path = './report/' + now + '.html'

fm = open(report_path, 'wb')
HTMLTestReportCN.HTMLTestRunner(stream=fm, title='接口自动化报告', tester="王帅龙", verbosity=2).run(suite)

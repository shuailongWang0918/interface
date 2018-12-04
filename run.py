import HTMLTestReportCN
import time
from Event.client import *
from xml.etree.ElementTree import ElementTree as ET

suite = unittest.TestSuite()

doc = ET().parse(source='./config.xml')
li = doc.findall('./cases/*')

for l in li:
    classname = l.tag.split('-')[0]
    methodname = l.tag.split('-')[1]
    CASES_INFO = '''from Event.cases.{classname} import {classname}
suite.addTest({classname}("test_{methodname}"))'''.format(classname=classname, methodname=methodname)
    exec(CASES_INFO)

now = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
report_path = './report/' + now + '.html'

fm = open(report_path, 'wb')
HTMLTestReportCN.HTMLTestRunner(stream=fm, title='接口自动化报告', tester="王帅龙", verbosity=2).run(suite)

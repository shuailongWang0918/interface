from Event.client import *
from ddt import ddt, data, file_data, unpack

"""
引入ddt包,实现数据驱动
导入外部json文件,实现一套代码运行多次,正向测试,逆向测试
"""


@ddt
class dome04(unittest.TestCase):
    """登录接口用例"""
    url = 'http://139.199.132.220:9000/event/api/register/'

    def setUp(self):
        self.client = Client(url=self.url, method='POST', body_type=BodyType.URL_ENCODE)

    @file_data('../datajson/regster01.json')
    def test_register01(self, username, password, asserts, info):
        """登录接口正向流程用例"""
        client = self.client
        username = username
        password = password
        data = {'username': username, 'password': password}
        client.set_body(data)
        client.send()
        client.check_status_code_is_200()
        client.check_json_value('error_code', asserts)
        text = client.res_text
        print(info)

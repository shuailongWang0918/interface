import requests
import unittest

"""
需要先安装 requests 和 unittest
python包 python版本3.6.5
"""


class BodyType:
    """定义接口传输正文体数据类型"""
    URL_ENCODE = 1
    FORM = 2
    XML = 3
    JSON = 4


class Client(unittest.TestCase):
    def __init__(self, url, method='get', body_type=0, params=None):
        """初始化函数,url为必填项,method默认为get请求,可填get和post请求,body_type为正文体格式"""
        self.url = url
        self.method = method
        self.body_type = body_type
        self.headers = {}
        self.params = params
        self.res = None
        self._type_equality_funcs = {}

    def set_headers(self, headers):
        """headers头信息必须是字典格式"""
        if isinstance(headers, dict):
            self.headers = headers
        else:
            raise Exception('头信息不是字典格式')

    def set_header(self, key, value):
        """直接以key/value方式添加头信息"""
        self.headers[key] = value

    def set_body(self, body):
        """根据body_type判断用户选择的正文数据传递方式"""
        if isinstance(body, dict):
            if self.body_type == 1:
                self.set_header("Content-type", "application/x-www-form-urlencoded")
            elif self.body_type == 3:
                self.set_header("Content", "application/xml")
            elif self.body_type == 4:
                self.set_header("Content", "application/json")
            else:
                raise Exception('正文格式参数错误')
            self.body = body

        else:
            raise Exception('正文不是字典格式，字典格式如下：{"key":"value"}')

    def send(self):
        """发送请求"""
        self.method = self.method.upper().strip()
        if self.method == "GET":
            self.res = requests.get(url=self.url, headers=self.headers, params=self.params)
        elif self.method == "POST":
            if self.body_type == 1 or self.body_type == 2:
                self.res = requests.post(url=self.url, headers=self.headers, data=self.body)
            elif self.body_type == 3:
                xml = self.body.get("xml")
                self.res = requests.post(url=self.url, headers=self.headers, data=xml)
            elif self.body_type == 4:
                self.res = requests.post(url=self.url, headers=self.headers, json=self.body)
            elif self.body_type == 5:
                self.res = requests.post(url=self.url, headers=self.headers, files=self.body)
            elif self.body_type == 0:
                self.res = requests.post(url=self.url, headers=self.headers)
            else:
                raise Exception("正文格式参数错误")
        else:
            raise Exception("只支持GET和POST请求")

    @property
    def status_code(self):
        """返回HTTP请求状态码"""
        if self.res:
            return self.res.status_code
        else:
            return None

    @property
    def res_time(self):
        """返回请求响应时间"""
        if self.res:
            return self.res.elapsed.microseconds / 1000
        else:
            return None

    @property
    def res_text(self):
        """返回请求响应数据"""
        if self.res:
            return self.res.text
        else:
            return None

    @property
    def res_to_json(self):
        """返回数据转为json格式"""
        if self.res:
            return self.res.json()
        else:
            return None

    def check_status_code_is_200(self):
        """判断状态码是否为200"""
        self.assertEqual(self.status_code, 200, '响应状态码不是200')

    def check_status_code_is(self, code):
        """判断状态码"""
        self.assertEqual(self.status_code, code, '响应状态码不是%d' % code)

    def check_res_time_less_than(self, times=200):
        """判断响应时间是否大于200ms"""
        self.assertLess(self.res_time, times, '响应时间超过 %d ms' % times)

    def check_json_value(self, path, exp):
        """判断返回数据中是否包含预期结果"""
        if self.res_to_json:
            first = self.res_to_json.get(path)
        else:
            first = None
        self.assertEqual(first, exp, '检查失败.实际结果:{first}预期结果:{exp}'.format(first=first, exp=exp))

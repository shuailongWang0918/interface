import pymysql

# from Event.client import *
#
#
# url = "http://ws.webxml.com.cn/WebServices/WeatherWS.asmx/getRegionCountry"
# client = Client(url=url, method="post", body_type=body_type.URL_ENCODE)
# client.set_body({})
# client.send()
# print(client.status_code)
# print(client.res_time)
# # print(client.res_text)


connect = pymysql.connect(host='139.199.132.220', port=3306, db='event', user='root', password='123456')
cursor = connect.cursor()
cursor.execute('select * from api_event')
print(cursor.fetchall())
connect.close()

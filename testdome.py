from Event.client import *

url = "http://0.0.0.0"
client = Client(url=url, method="post", body_type=body_type.URL_ENCODE)
client.set_body({})
client.send()
print(client.status_code)
print(client.res_time)
print(client.res_text)

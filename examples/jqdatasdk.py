import re
from datetime import datetime
from http.cookies import SimpleCookie
from pprint import pprint

from jupyter_kernel_client import KernelClient

from jupyter_data_fetch.codec import extract_from_reply
from jupyter_data_fetch.wraps.jqdatasdk import *

COOKIE = 'user-12345678901=2|1:0|10:1782905738|16:user-12345678901|48:ZTMxZTBmYTYtNjVkOC00ZmQ2LWI2YmItNmY4NmNhODRlOWQ0|0eaeaafc6b33e898d5905d879d9c85b5a0b256930c29b755b3f2ce15f7b1c5bb; uid=wKiXm2jC68o2sUDuZ0rwAg==; getStrategy=1; _xsrf=2|a0420526|3ad949c771bac9911b1012232f89763b|1782461011; token=2920d269ae8cbd6a1f3fdc0d725bf3bc4d3a2697; PHPSESSID=5r217s9lc1afeqe41u3m3milq1'
HEADERS = {'Cookie': COOKIE, 'X-XSRFToken': SimpleCookie(COOKIE)['_xsrf'].value}
UID = re.search(r'user-(\d+)=', COOKIE).group(1)
SERVER_URL = f"https://www.joinquant.com/user/{UID}"
NAME = "python3"
PATH = "/home/jquser"

kernel = KernelClient(server_url=SERVER_URL, token=None, headers=HEADERS)
kernel.start(name=NAME, path=PATH)
pprint(kernel.list_kernels())

LazyKernel.set_kernel(kernel)

reply = kernel.execute("""!pwd""")
print(extract_from_reply(reply))  # 注意：start中path没生效

reply = kernel.execute(f"""
import os
os.chdir({repr(PATH)})
print(os.getcwd())

# import jqresearch_query
""")
print(extract_from_reply(reply))  # 修改当前目录

df = get_industry(security=['000001.XSHE', '000002.XSHE'], date="2018-06-01")
print(df)
df = get_extras('is_st', ['000001.XSHE', '000018.XSHE'], start_date='2013-12-01', end_date='2013-12-03')
print(df)
df = get_all_securities(['stock'], datetime.today())
print(df)
df = get_price('000001.XSHE')
print(df)
df = get_security_info('000001.XSHE')
print(df)
print(df.display_name)
df = get_fundamentals("query(valuation, income).filter(valuation.code.in_(['000001.XSHE', '600000.XSHG']))", date='2022-01-20')
print(df)
df = get_index_weights(index_id="000001.XSHG", date="2018-05-09")
print(df)

kernel.stop()

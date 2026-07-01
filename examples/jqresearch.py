# Notebook中可以通过help()获得函数签名
# 为了演示，集中在一个文件。建议用户自己使用时独立到其他文件
import re

from jupyter_data_fetch.wraps import auto_execute


# 定义函数
@auto_execute
def get_all_securities(types=[], date=None):
    # stocks = get_all_securities(['stock', 'index'], '2026-06-01') # 支持
    # get_all_securities(['stock', 'index'],  datetime.today()) # 不支持。需要回退到kernel.execute, 先from datetime import datetime
    pass


@auto_execute
def get_price(security, start_date=None, end_date=None, frequency='daily', fields=None, skip_paused=False, fq='pre', count=None, panel=True, fill_paused=True, round=True):
    pass


# ===============================================================================

from http.cookies import SimpleCookie

from jupyter_kernel_client import KernelClient

COOKIE = 'user-12345678901=2|1:0|10:1782905738|16:user-12345678901|48:ZTMxZTBmYTYtNjVkOC00ZmQ2LWI2YmItNmY4NmNhODRlOWQ0|0eaeaafc6b33e898d5905d879d9c85b5a0b256930c29b755b3f2ce15f7b1c5bb; uid=wKiXm2jC68o2sUDuZ0rwAg==; getStrategy=1; _xsrf=2|a0420526|3ad949c771bac9911b1012232f89763b|1782461011; token=2920d269ae8cbd6a1f3fdc0d725bf3bc4d3a2697; PHPSESSID=5r217s9lc1afeqe41u3m3milq1'
HEADERS = {'Cookie': COOKIE, 'X-XSRFToken': SimpleCookie(COOKIE)['_xsrf'].value}
UID = re.search(r'user-(\d+)=', COOKIE).group(1)
SERVER_URL = f"https://www.joinquant.com/user/{UID}"

with KernelClient(server_url=SERVER_URL, token=None, headers=HEADERS) as kernel:
    from jupyter_data_fetch.codec import LazyKernel

    LazyKernel.set_kernel(kernel)

    df = get_all_securities(['stock', 'index'], '2026-06-01')
    print(df)
    df = get_price('000001.XSHE')
    print(df)

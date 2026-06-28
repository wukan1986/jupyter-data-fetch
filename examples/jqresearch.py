# Notebook中可以通过help()获得函数签名
# 为了演示，集中在一个文件。建议用户自己使用时独立到其他文件
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

Cookie = 'user-12345678901=2|1:0|10:1782612273|16:user-12345678901|48:NzA0ODFkNzItYWJkYi00Njg4LThkMDQtN2Y0M2NmODY0NGYw|52b0c3efe3112d34e67eb2728a1fd231aceb117a575d90177672553f67a847b6; uid=wKiXm2jC68o2sUDuZ0rwAg==; getStrategy=1; _xsrf=2|a0420526|3ad949c771bac9911b1012232f89763b|1782461011; token=2824ee78d21e17124b752edb6905c908b3892e78; PHPSESSID=io3t5iqtd22g6lbgfb47m6bb94'

headers = {'Cookie': Cookie, 'X-XSRFToken': SimpleCookie(Cookie)['_xsrf'].value}

with KernelClient(server_url="https://www.joinquant.com/user/12345678901", token=None, headers=headers) as kernel:
    from jupyter_data_fetch.codec import LazyKernel

    LazyKernel.set_kernel(kernel)

    df = get_all_securities(['stock', 'index'], '2026-06-01')
    print(df)
    df = get_price('000001.XSHE')
    print(df)

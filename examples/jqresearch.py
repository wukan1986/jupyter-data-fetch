# Notebook中可以通过help()获得函数签名
# 为了演示，集中在一个文件。建议用户自己使用时独立到其他文件
from jupyter_date_fetch.codec import auto_execute


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

Cookie = 'user-26702897463=2|1:0|10:1782347474|16:user-26702897463|48:MDljZjM0NTYtYWMyOS00MTJhLWIxZDItNjJmZmFhNGQ3Mzkz|858778c0b00b7a1fa5a07330e0197e2961ce2224f947b23dc73382983f3b03a0; uid=wKiXm2o8DlhXTgWbgjO+Ag==; _xsrf=2|0164e5f2|038f6ab01e86f30cd8149a199a40e6ae|1782321118; token=7d6a38a8531680694fad56ec4cf04bbf62ffdb19; PHPSESSID=o90iesn2g9thepf989s3nlhit5'

headers = {'Cookie': Cookie, 'X-XSRFToken': SimpleCookie(Cookie)['_xsrf'].value}

with KernelClient(server_url="https://www.joinquant.com/user/26702897463", token=None, headers=headers) as kernel:
    from jupyter_date_fetch.codec import LazyKernel

    LazyKernel.set_kernel(kernel)

    stocks = get_all_securities(['stock', 'index'], '2026-06-01')
    print(stocks)
    prices = get_price('000001.XSHE')
    print(prices)

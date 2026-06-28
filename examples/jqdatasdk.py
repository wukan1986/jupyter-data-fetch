from datetime import datetime
from http.cookies import SimpleCookie
from pprint import pprint

from jupyter_kernel_client import KernelClient

from jupyter_data_fetch.wraps.jqdatasdk import *

Cookie = 'user-12345678901=2|1:0|10:1782525641|16:user-12345678901|48:MzE5M2ZlZjEtYzYzYi00N2U5LWJmZWItZGY4ZGIzMzYyYjk3|e5ad5553c75aadb148ddff8fcf7c44f69a8d69e6f0ae83b5c0cafb26f1e003f3; uid=wKiXm2jC68o2sUDuZ0rwAg==; getStrategy=1; _xsrf=2|a0420526|3ad949c771bac9911b1012232f89763b|1782461011; token=93125ac7b2edebc15619c3f7cdd186befcae809b; PHPSESSID=i0jls09cd4uabmat6hdiugdp96'
headers = {'Cookie': Cookie, 'X-XSRFToken': SimpleCookie(Cookie)['_xsrf'].value}

with KernelClient(server_url="https://www.joinquant.com/user/12345678901", token=None, headers=headers) as kernel:
    pprint(kernel.list_kernels())

    from jupyter_data_fetch.codec import LazyKernel, extract_from_reply

    LazyKernel.set_kernel(kernel)

    reply = kernel.execute("""!pwd""")
    print(extract_from_reply(reply))  # 注意：未指定kernels时，当前目录是/

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

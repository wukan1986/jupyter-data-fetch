import re
from http.cookies import SimpleCookie

from jupyter_kernel_client import KernelClient

from jupyter_data_fetch.codec import JupyterTextCodec, JupyterImageCodec

COOKIE = 'user-12345678901=2|1:0|10:1782905738|16:user-12345678901|48:ZTMxZTBmYTYtNjVkOC00ZmQ2LWI2YmItNmY4NmNhODRlOWQ0|0eaeaafc6b33e898d5905d879d9c85b5a0b256930c29b755b3f2ce15f7b1c5bb; uid=wKiXm2jC68o2sUDuZ0rwAg==; getStrategy=1; _xsrf=2|a0420526|3ad949c771bac9911b1012232f89763b|1782461011; token=2920d269ae8cbd6a1f3fdc0d725bf3bc4d3a2697; PHPSESSID=5r217s9lc1afeqe41u3m3milq1'
HEADERS = {'Cookie': COOKIE, 'X-XSRFToken': SimpleCookie(COOKIE)['_xsrf'].value}
UID = re.search(r'user-(\d+)=', COOKIE).group(1)
SERVER_URL = f"https://www.joinquant.com/user/{UID}"

with KernelClient(server_url=SERVER_URL, token=None, headers=HEADERS) as kernel:
    code = """
df = get_fundamentals(query(
        valuation, income
    ).filter(
        # 这里不能使用 in 操作, 要使用in_()函数
        valuation.code.in_(['000001.XSHE', '600000.XSHG'])
    ), date='2015-10-15')
"""
    reply = kernel.execute(JupyterTextCodec.generate_code(code, var_name='df'), store_history=False)
    # print(reply)
    obj = JupyterTextCodec.extract_decode(reply)
    print(obj)

    reply = kernel.execute(JupyterImageCodec.generate_code(var_name='df'), store_history=False)
    # print(reply)
    obj = JupyterImageCodec.extract_decode(reply)
    print(obj)

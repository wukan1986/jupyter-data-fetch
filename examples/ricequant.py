from http.cookies import SimpleCookie
from pprint import pprint

from jupyter_kernel_client import KernelClient

from jupyter_date_fetch.codec import JupyterBase85Codec, JupyterImageCodec

Cookie = 'jupyterhub-user-user_123456=2|1:0|10:1782310843|27:jupyterhub-user-user_123456|40:bUZzWVBSeDcxdXFmRjFtdUI3dDFsSTA5ZVE1ZEVO|856cf571f52f5753f99cb96ff164375215cb432f820d1cf36deba0a341cac167; tgw_l7_route=006b76bf4a6398f05baf657858ca2891; jupyter-hub-token=; sid=apG2XqdJttarfl255exP8hevHMjPTVSS|3b2370a8c4f723d6e2280d640cfff0e85f882fd17a66b842a8c358cab3cc61395f4932f854c93a9d093c6b7b13554385ec8e6e603dd51fa443a17ca4c64b8b8a; jupyterhub-session-id=0e48f1a1974a45f08e99ad50ba84fd06; jupyterhub-hub-login="2|1:0|10:1782310842|20:jupyterhub-hub-login|44:NjdhMzIxMTk3ODI3NGMyYzgyN2FiYjA3YTcwNTI2NWY=|cc6c11d238bd028fd336fb567c3d16921431cc365cfa74123a22047f7e59b21e"; _xsrf=2|a1261e8f|51fe49f9992506a09880bb28853f3b28|1782310843; Hm_lvt_cb81fd54150b99e25d085d58bbaf4a07=1782310842; HMACCOUNT=54C5A216213487CB; Hm_lpvt_cb81fd54150b99e25d085d58bbaf4a07=1782310859'

headers = {'Cookie': Cookie, 'X-XSRFToken': SimpleCookie(Cookie)['_xsrf'].value}

with KernelClient(server_url="https://www.ricequant.com/research/user/user_123456", token=None, headers=headers) as kernel:
    pprint(kernel.list_kernels())
    # 使用python3.9，不要使用python 3.6
    kernel_id = kernel.list_kernels()[0]['id']

with KernelClient(server_url="https://www.ricequant.com/research/user/user_123456", token=None, headers=headers, kernel_id=kernel_id) as kernel:
    code = """
df = get_industry('621020', source='citics_2019', date=None, market='cn')
"""
    reply = kernel.execute(JupyterBase85Codec.generate_code(code))
    # print(reply)
    obj = JupyterBase85Codec.extract_decode(reply)
    print(obj)

    reply = kernel.execute(JupyterImageCodec.generate_code())
    # print(reply)
    obj = JupyterImageCodec.extract_decode(reply)
    print(obj)

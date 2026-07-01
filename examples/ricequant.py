import re
from http.cookies import SimpleCookie
from pprint import pprint

from jupyter_kernel_client import KernelClient

from jupyter_data_fetch.codec import JupyterTextCodec, JupyterImageCodec, extract_from_reply

COOKIE = 'jupyterhub-user-user_123456=2|1:0|10:1782907352|27:jupyterhub-user-user_123456|40:N1JqSjhYSmRuSkJPa3M0MHc4SXIzcEszbVQ3aWUx|a409e6e517378f4b8347ed356b64a35cf012cdb1fb64aa63896975bd298ebf9c; tgw_l7_route=3596f940fbcd94bd2bec34c51be04477; jupyter-hub-token=; sid=nNhHlJmIPZknb6A1WGJfcdiIkHVQfyIN|2410a5a736e615894ca18cec519f605dc6d4c5fb28e79925d05c332b541061a9f3812adce1d0ec0e1721888c05fcc13a828f907e31cd57bdcb1f75dae4cf7e30; jupyterhub-session-id=77d3aa9f793c421fb7e80c9db3067476; jupyterhub-hub-login="2|1:0|10:1782907352|20:jupyterhub-hub-login|44:NjdhMzIxMTk3ODI3NGMyYzgyN2FiYjA3YTcwNTI2NWY=|180f723e8e52e79e471f5addb1ba8c2e1faf278532d9d6ea3878057734f083f7"; _xsrf=2|b6ad5052|c49eba51ef6ae3ecfab93c97c122e2a8|1782907352; Hm_lvt_cb81fd54150b99e25d085d58bbaf4a07=1782907354; HMACCOUNT=FD9E0D86AB8815CB; Hm_lpvt_cb81fd54150b99e25d085d58bbaf4a07=1782907380'
HEADERS = {'Cookie': COOKIE, 'X-XSRFToken': SimpleCookie(COOKIE)['_xsrf'].value}
UID = re.search(r'user_\d+', COOKIE).group(0)
SERVER_URL = f"https://www.ricequant.com/research/user/{UID}"
NAME = "python3.9"  # 使用python3.9，不要使用python 3.6
PATH = "/home/rice/notebook"

kernel = KernelClient(server_url=SERVER_URL, token=None, headers=HEADERS)
kernel.start(name=NAME, path=PATH) # path没有生效，得道
pprint(kernel.list_kernels())

reply = kernel.execute("""!pwd""")
print(extract_from_reply(reply))  # 注意：未指定kernels时，当前目录是/tmp

code = """
df = get_industry('621020', source='citics_2019', date=None, market='cn')
"""
reply = kernel.execute(JupyterTextCodec.generate_code(code), store_history=False)
# print(reply)
obj = JupyterTextCodec.extract_decode(reply)
print(obj)

reply = kernel.execute(JupyterImageCodec.generate_code(), store_history=False)
# print(reply)
obj = JupyterImageCodec.extract_decode(reply)
print(obj)

kernel.stop()

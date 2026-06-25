from http.cookies import SimpleCookie

from jupyter_kernel_client import KernelClient

from jupyter_date_fetch.codec import JupyterBase85Codec, JupyterImageCodec

Cookie = 'username-127-0-0-1-8888="2|1:0|10:1782285725|23:username-127-0-0-1-8888|216:eyJ1c2VybmFtZSI6ICI0ZDI0NjhhNDMxM2Y0ZGRmYjZhY2YyOWZjOGQ4NjEwYiIsICJuYW1lIjogIkFub255bW91cyBLb3JlIiwgImRpc3BsYXlfbmFtZSI6ICJBbm9ueW1vdXMgS29yZSIsICJpbml0aWFscyI6ICJBSyIsICJjb2xvciI6IG51bGwsICJhdmF0YXJfdXJsIjogbnVsbH0=|907cc4cca8ab74fe24418030aced6438ba0ab80a71b045335855aa36ae549d70"; _xsrf=2|812eeb93|3c523de36482f81360b05b8ecbf789fa|1782285725'

headers = {'Cookie': Cookie, 'X-XSRFToken': SimpleCookie(Cookie)['_xsrf'].value}

kernel = KernelClient(server_url="http://127.0.0.1:8888", token=None, headers=headers)
kernel.start()

code = """
import pandas as pd
df = pd.DataFrame({'A':[1,2,3,4, 6]})
"""
reply = kernel.execute(JupyterBase85Codec.generate_code(code, var_name='df'))
# print(reply)
obj = JupyterBase85Codec.extract_decode(reply)
print(obj)

reply = kernel.execute(JupyterImageCodec.generate_code(var_name='df'))
# print(reply)
obj = JupyterImageCodec.extract_decode(reply)
print(obj)

kernel.stop()

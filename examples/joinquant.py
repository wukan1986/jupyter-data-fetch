from http.cookies import SimpleCookie

from jupyter_kernel_client import KernelClient

from jupyter_data_fetch.codec import JupyterTextCodec, JupyterImageCodec

Cookie = 'jupyterhub-user-user_241308=2|1:0|10:1782310843|27:jupyterhub-user-user_241308|40:bUZzWVBSeDcxdXFmRjFtdUI3dDFsSTA5ZVE1ZEVO|856cf571f52f5753f99cb96ff164375215cb432f820d1cf36deba0a341cac167; user-12345678901=2|1:0|10:1782321118|16:user-12345678901|48:YTc2N2RkMDctNzA2Zi00MjQ3LWE1MzMtNDBhNjBmOGUzY2Mw|fda673eb86884a9ce684270a5c92d75c760dc38201ddd9d01c7d4b71f441e7e3; jupyter-hub-token="2|1:0|10:1782321118|17:jupyter-hub-token|44:YzAwYTI1YTYxMjA0NGFlYWI0YjNiOWE5YzU4MGZjYzc=|d9f4ca92e7132c5c8fe25207ef9cdd6e3a8f7e1c2f036afaf12ff5694b48aca0"; qgqp_b_id=d4739e953f7db59b71c6853ba3be1195; st_nvi=cWzWd5QeSAiiwJsLtS3ywe0aa; st_pvi=28911970663629; st_sp=2026-06-24%2015%3A20%3A56; st_inirUrl=; nid18=0666ec0c9049947327f4af06b44bbf39; nid18_create_time=1782285657433; gviem=fMwPu3z3RGcMkCEpmqenk10f5; gviem_create_time=1782285657433; username-127-0-0-1-8888="2|1:0|10:1782285725|23:username-127-0-0-1-8888|216:eyJ1c2VybmFtZSI6ICI0ZDI0NjhhNDMxM2Y0ZGRmYjZhY2YyOWZjOGQ4NjEwYiIsICJuYW1lIjogIkFub255bW91cyBLb3JlIiwgImRpc3BsYXlfbmFtZSI6ICJBbm9ueW1vdXMgS29yZSIsICJpbml0aWFscyI6ICJBSyIsICJjb2xvciI6IG51bGwsICJhdmF0YXJfdXJsIjogbnVsbH0=|907cc4cca8ab74fe24418030aced6438ba0ab80a71b045335855aa36ae549d70"; _xsrf=2|812eeb93|3c523de36482f81360b05b8ecbf789fa|1782285725; jupyter-hub-token=; sid=apG2XqdJttarfl255exP8hevHMjPTVSS|3b2370a8c4f723d6e2280d640cfff0e85f882fd17a66b842a8c358cab3cc61395f4932f854c93a9d093c6b7b13554385ec8e6e603dd51fa443a17ca4c64b8b8a; jupyterhub-session-id=0e48f1a1974a45f08e99ad50ba84fd06; jupyterhub-hub-login="2|1:0|10:1782310842|20:jupyterhub-hub-login|44:NjdhMzIxMTk3ODI3NGMyYzgyN2FiYjA3YTcwNTI2NWY=|cc6c11d238bd028fd336fb567c3d16921431cc365cfa74123a22047f7e59b21e"; _xsrf=2|a1261e8f|51fe49f9992506a09880bb28853f3b28|1782310843; HMACCOUNT_BFESS=54C5A216213487CB; Hm_lvt_cb81fd54150b99e25d085d58bbaf4a07=1782310842; HMACCOUNT=54C5A216213487CB; Hm_lpvt_cb81fd54150b99e25d085d58bbaf4a07=1782313178; tgw_l7_route=006b76bf4a6398f05baf657858ca2891; NID=532=ZE88MhgaFdDpOAM1UHXS0G3NXjsvkCt4LGmY8SzhZA10QQQzgmzLKmoOfXXt_0R-6YU8XFHLDybOF-m1ip_2YlhXWFjxBjc42hbq2Eq8JojlapwCkx5yoA41D549I-KzW4bGfyGSTJddBRlLcVcyMsLjR7guNgZMZLYK92j62qKhzaFhIfYUDw_f-6f3FbvVk5sT6w; uid=wKiXm2o8DlhXTgWbgjO+Ag==; token=203e08cc23dae4bb682da0f3baab1fbfc0729d48; uid=wKgyrWo8Dlx7HQW2rp7BAg==; PHPSESSID=sftkl11ru1nr6nt6olbv31bfj6; _xsrf=2|0164e5f2|038f6ab01e86f30cd8149a199a40e6ae|1782321118'

headers = {'Cookie': Cookie, 'X-XSRFToken': SimpleCookie(Cookie)['_xsrf'].value}

with KernelClient(server_url="https://www.joinquant.com/user/12345678901", token=None, headers=headers) as kernel:
    code = """
df = get_fundamentals(query(
        valuation, income
    ).filter(
        # 这里不能使用 in 操作, 要使用in_()函数
        valuation.code.in_(['000001.XSHE', '600000.XSHG'])
    ), date='2015-10-15')
"""
    reply = kernel.execute(JupyterTextCodec.generate_code(code, var_name='df'))
    # print(reply)
    obj = JupyterTextCodec.extract_decode(reply)
    print(obj)

    reply = kernel.execute(JupyterImageCodec.generate_code(var_name='df'))
    # print(reply)
    obj = JupyterImageCodec.extract_decode(reply)
    print(obj)

from http.cookies import SimpleCookie

from jupyter_kernel_client import KernelClient

from jupyter_data_fetch.codec import JupyterTextCodec, JupyterImageCodec, extract_from_reply

# 超时时间短，需要常更新
Cookie = '_xsrf=2|85a84a35|4efa22c2067b973c48553348f101f8bc|1782301797; jupyterhub-user-123456789=2|1:0|10:1782310633|25:jupyterhub-user-123456789|40:S0t5cUtkZ3dhc0NiaDQwNEVFc3dwa2lLem90d0x6|52ed55bc081e8f02853919bcebe61ec62c5b392a7a2553bf359ddd90e52c97a9; _ga=GA1.1.926941427.1782301674; _ga_H2RK0R0681=GS2.1.s1782301673$o1$g0$t1782301697$j36$l0$h0; u_ukey=A10702B8689642C6BE607730E11E6E4A; u_uver=1.0.0; u_dpass=8IbAWbGAubzxNJ2uPWPZZALzSjlxV4lNGIQvX3QpukmKP9eMyTCCk9LRH8GOrdeSHi80LrSsTFH9a%2B6rtRvqGg%3D%3D; u_did=CAB895BDFF094A8A8CAE2F908CF48CAB; u_ttype=WEB; ttype=WEB; user=MDpteF90ZzYyYW5ld206Ok5vbmU6NTAwOjg2MjAxNjg0Mzo3LDExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoxNjo6Ojg1MjAxNjg0MzoxNzgyMzAxNzg4Ojo6MTc3MzEzNjYyMDo2MDQ4MDA6MDoxN2Q2YTQ1M2IwODZjZDhmYzVlOGQwNWNmNjEwZmU0Mjg6ZGVmYXVsdF81OjA%3D; userid=123456789; u_name=mx_tg62anewm; escapename=mx_tg62anewm; ticket=bb780ea2cfe6e331d91e069efe244c95; user_status=0; utk=a38d3317371ba460dc713a20be855272; sess_tk=eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiIsImtpZCI6InNlc3NfdGtfMSIsImJ0eSI6InNlc3NfdGsifQ.eyJqdGkiOiIyOGU0MGY2MWNmMDU4ZDVlZmNkODZjMDgzYjQ1NmE3ZDEiLCJpYXQiOjE3ODIzMDE3ODgsImV4cCI6MTc4MjkwNjU4OCwic3ViIjoiODUyMDE2ODQzIiwiaXNzIjoidXBhc3MuMTBqcWthLmNvbS5jbiIsImF1ZCI6IjIwMjAxMTE4NTI4ODkwNzIiLCJhY3QiOiJvZmMiLCJjdWhzIjoiMTQ0N2JkYWFkYmQ0NWI1OWM2M2NlYTRjZDI1ZGQ5ZTE1YmJmOTA2M2RhMjUwNDkzNjA4YWE2NzdkNGU1ZjIzYiJ9.vy6ifxYCP1e0s8Q7NXQb4gDkHTHnfi2ODG8MjjeQVi1PKwxmWCR1jr5QpdWGTzwLFhJbLMICBcwXxsh3IgwUKA; cuc=9whwt1dc5pu3; jupyterhub-session-id=f9a0274fec8c45408cafc1b49ccad06c; quantoken=45ed248fa1e7327a1d0aa73fd739fd0dfb78b4a20fd76f518c96ae431b022d9e38a06be26a84e4dd24d0e8831515261f20c86acdc62ff49f1f7e0705ed950047949d10c96e7d5ffe1821069e86bd22d8; v=A09etmBLeX39EH0BhhWCGIbA3uhcdKOWPcinimFc677FMGGWaUQz5k2YN8Fy; _ga_KQBDS1VPQF=GS2.1.s1782310623$o3$g1$t1782310624$j59$l0$h0'
headers = {'Cookie': Cookie, 'X-XSRFToken': SimpleCookie(Cookie)['_xsrf'].value}

with KernelClient(server_url="https://supermind.10jqka.com.cn/notebook/user/123456789", token=None, headers=headers) as kernel:
    code = """
import collections

print(collections._sys.version)
"""
    reply = kernel.execute(code)
    obj = extract_from_reply(reply)
    print(obj)

    code = """
df = query_iwencai("近10日的区间主力资金流向>5000万元，市值>1000亿，日成交额>30亿")
"""
    reply = kernel.execute(JupyterTextCodec.generate_code(code, var_name='df'), store_history=False)
    # print(reply)
    obj = JupyterTextCodec.extract_decode(reply)
    print(obj)

    reply = kernel.execute(JupyterImageCodec.generate_code(var_name='df'), store_history=False)
    # print(reply)
    obj = JupyterImageCodec.extract_decode(reply)
    print(obj)

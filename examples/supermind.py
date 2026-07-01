import re
from http.cookies import SimpleCookie

from jupyter_kernel_client import KernelClient

from jupyter_data_fetch.codec import JupyterTextCodec, JupyterImageCodec, extract_from_reply

# 超时时间短，需要常更新
COOKIE = '_xsrf=2|d4868d15|1caa2d911afa1895a8eccbd52ecd5855|1782786648; jupyterhub-user-123456789=2|1:0|10:1782912581|25:jupyterhub-user-123456789|40:Wkx6NURCZ2hFeERvNTEwREF5Y2NtYXhDWXFTVDBk|41cb64955fb01174f929c511ce2fa40d6cc39984be12d4dcf88633e2796167e2; searchGuide=sg; _ga=GA1.1.1338585586.1770875522; Hm_lvt_69929b9dce4c22a060bd22d703b2a280=1770875520,1770878330,1770945448,1771852122; Hm_lvt_722143063e4892925903024537075d0d=1770875649,1770878341,1770945452,1771852127; Hm_lvt_929f8b362150b1f77b477230541dbbc2=1770875650,1770878341,1770945452,1771852127; Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1770875538,1770878341,1770945452,1771852127; _ga_H2RK0R0681=GS2.1.s1773045131$o4$g1$t1773045181$j10$l0$h0; u_ukey=A10702B8689642C6BE607730E11E6E4A; u_uver=1.0.0; u_dpass=qTEymopshH8oPNnaCk90ecz41sj4E694TcHx0jRpSvBafdIyaCRABqAmBagIodttHi80LrSsTFH9a%2B6rtRvqGg%3D%3D; u_did=4F3BCD0DF64042799BA50142F8DF9112; u_ttype=WEB; user=MDpteF90ZzYyYW5ld206Ok5vbmU6NTAwOjg2MjAxNjg0Mzo3LDExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoxNjo6Ojg1MjAxNjg0MzoxNzgyNzg2NjAxOjo6MTc3MzEzNjYyMDo2MDQ4MDA6MDoxZGM0YTE2ZGMwZWRhZjE4OGZkMzU0YWJlMTFjZWZkOWQ6ZGVmYXVsdF81OjA%3D; userid=123456789; u_name=mx_tg62anewm; escapename=mx_tg62anewm; ticket=bc2486eb09cb41a84499e6f22811ccf7; user_status=0; utk=5f5e84935b3c6aaadfb9d46e6e6e7690; sess_tk=eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiIsImtpZCI6InNlc3NfdGtfMSIsImJ0eSI6InNlc3NfdGsifQ.eyJqdGkiOiI5ZGZkY2UxMWJlNGEzNWZkODhmMWRhMGVkYzE2NGFkYzEiLCJpYXQiOjE3ODI3ODY2MDEsImV4cCI6MTc4MzM5MTQwMSwic3ViIjoiODUyMDE2ODQzIiwiaXNzIjoidXBhc3MuMTBqcWthLmNvbS5jbiIsImF1ZCI6IjIwMjAxMTE4NTI4ODkwNzIiLCJhY3QiOiJvZmMiLCJjdWhzIjoiMGMyNDFlZGU3YTMyNTVhOWQ3NzBjNWUyNTcwM2IxNGJiZGViMTBiOWJiODQ0YmY1OWNmOThjNmQ4MjU5ZmY1MyJ9.EmVninUHquJJY3D4-w94yW8es1xjV4Fom8W5LMxS4vwsbxdt9Wkxw2ogCHAewXHQYV79tXO6OXfrJ8QEp9R1OA; cuc=xtiuhm7v9pap; v=BNHy5vctQ43Qa0NWKtpqwQtkClUADwBSAAkAZADTAAYA46S4ACv4-f8RAUkAGwAuAHUAIADd; quantoken=45ed248fa1e7327a1d0aa73fd739fd0d4b3e6d652164ad4877bdd823dfd88d489faa2397da156224cb1bae79dceec78286e1e1a8fd47f04b3bf8852a33d7aba87c3766a5695d96732dd07026f36458eb; jupyterhub-session-id=2882f3840ab149b3b76911206d11fa31; _ga_KQBDS1VPQF=GS2.1.s1782912568$o28$g0$t1782912568$j60$l0$h0'
HEADERS = {'Cookie': COOKIE, 'X-XSRFToken': SimpleCookie(COOKIE)['_xsrf'].value}
UID = re.search(r'user-(\d+)=', COOKIE).group(1)
SERVER_URL = f"https://supermind.10jqka.com.cn/notebook/user/{UID}"

with KernelClient(server_url=SERVER_URL, token=None, headers=HEADERS) as kernel:
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

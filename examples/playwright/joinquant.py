import asyncio
import re
from http.cookies import SimpleCookie
from pprint import pprint

from jupyter_kernel_client import KernelClient

from jupyter_data_fetch.codec import JupyterTextCodec
from playwright_helper import AsyncBrowser, get_chrome_path, kill_browsers  # noqa

USERNAME = "13912345678"
PASSWORD = "123456"
NOTEBOOK = "9527.ipynb"  # 这个可以不提供

captured = {"url": None, "cookie": None}


async def capture_cookies():
    kill_browsers("chrome.exe")
    # kill_browsers("msedge.exe")

    async with AsyncBrowser(endpoint="http://127.0.0.1:9222", executable_path=get_chrome_path(), devtools=False, user_data_dir="D:\\user_data") as browser:
        page = await browser.get_page()

        async def on_request(request):
            if "api/kernelspecs" in request.url:
                captured["url"] = request.url
                captured["cookie"] = await request.header_value("cookie")
                print(captured)

        page.on("request", on_request)

        await page.goto("https://www.joinquant.com/research")
        await page.wait_for_load_state("networkidle")

        if "login" in page.url:
            await page.wait_for_load_state("domcontentloaded")
            await page.get_by_role("textbox", name="手机号").fill(USERNAME)
            await page.get_by_placeholder("请输入密码").fill(PASSWORD)
            await page.get_by_label("阅读并接受聚宽用户协议及隐私政策").check()
            await page.get_by_role("button", name="登 录").click()

        # 打开特定Notebook页，可屏蔽
        try:
            async with page.expect_popup(timeout=2000) as page1_info:
                await page.frame_locator("iframe[name=\"research\"]").get_by_role("link", name=NOTEBOOK).click(timeout=2000)
            await page.wait_for_load_state("networkidle")
        except:
            print(f"[跳过] 点击 notebook '{NOTEBOOK}' 超时，继续执行后续逻辑")


async def jupyter():
    COOKIE = captured['cookie']
    HEADERS = {'Cookie': COOKIE, 'X-XSRFToken': SimpleCookie(COOKIE)['_xsrf'].value}
    UID = re.search(r'user-(\d+)=', COOKIE).group(1)
    SERVER_URL = f"https://www.joinquant.com/user/{UID}"

    with KernelClient(server_url=SERVER_URL, token=None, headers=HEADERS) as kernel:
        pprint(kernel.list_kernels())

        code = """
df = get_fundamentals(query(
        valuation.code, valuation.market_cap, valuation.pe_ratio, income.total_operating_revenue
    ).filter(
        valuation.market_cap > 1000,
        valuation.pe_ratio < 10,
        income.total_operating_revenue > 2e10
    ).order_by(
        # 按市值降序排列
        valuation.market_cap.desc()
    ).limit(
        # 最多返回100个
        100
    ), date='2015-10-15')
"""

        reply = kernel.execute(JupyterTextCodec.generate_code(code, var_name='df'), store_history=False)
        # print(reply)
        obj = JupyterTextCodec.extract_decode(reply)
        print(obj)


async def main():
    await capture_cookies()
    await jupyter()


if __name__ == '__main__':
    asyncio.run(main())

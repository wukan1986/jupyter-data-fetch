"""
试验

在单元格中执行 print('Hello World')，可以记录日志
理论上是可以实现取数功能


需要研究code-server的通讯协议，后端与jupyter是不同的

"""
import asyncio
import msgpack

from playwright_helper import AsyncBrowser, get_chrome_path, kill_browsers  # noqa


async def main():
    # kill_browsers("chrome.exe")
    # kill_browsers("msedge.exe")

    async with AsyncBrowser(endpoint="http://127.0.0.1:9222", executable_path=get_chrome_path(), devtools=False, user_data_dir="D:\\user_data") as browser:
        page = await browser.get_page()

        # 定义 WebSocket 路由处理函数
        async def ws_handler(ws):
            print(ws.url)
            # 连接到真实的后端服务器
            server_ws = ws.connect_to_server()

            # 监听来自页面（客户端）的消息
            def on_page_message(message):
                if message[0] == 0x01:
                    # 将页面消息转发给真实服务器
                    if b'Hello World' in message:
                        print(msgpack.unpackb(message))
                        print(f"[PAGE -> SERVER]: {message}")
                server_ws.send(message)

            # 监听来自真实服务器的消息
            def on_server_message(message):
                if message[0] == 0x01:
                    if b'Hello World' in message:
                        print(f"[SERVER -> PAGE]: {message}")
                ws.send(message)

            # 绑定消息监听器
            ws.on_message(on_page_message)
            server_ws.on_message(on_server_message)

        # 拦截匹配 URL 的 WebSocket 连接
        await page.route_web_socket("**?reconnectionToken=*&reconnection=false*", ws_handler)
        await page.goto("https://bigquant.com/aistudio/studios/48ec8c2c-0f37-11ed-93bb-da75731aa77c/?folder=/home/aiuser/work")
        await asyncio.sleep(1000)
        await browser.close()


if __name__ == '__main__':
    asyncio.run(main())

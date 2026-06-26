"""本地测试

目前已经能从数据包中看到代码执行
"""
import asyncio
import json
import uuid

from jupyter_kernel_client.utils import deserialize_msg_from_ws_v1, deserialize_msg_from_ws_default, serialize_msg_to_ws_v1

from playwright_helper import AsyncBrowser, get_chrome_path, kill_browsers  # noqa


def pack(obj) -> bytes:
    return json.dumps(obj, separators=(",", ":"), sort_keys=True).encode("utf-8")


async def main():
    kill_browsers("chrome.exe")
    # kill_browsers("msedge.exe")

    async with AsyncBrowser(endpoint="http://127.0.0.1:9222", executable_path=get_chrome_path(), devtools=False, user_data_dir="D:\\user_data") as browser:
        page = await browser.get_page()

        # 定义 WebSocket 路由处理函数
        async def ws_handler(ws):
            # 连接到真实的后端服务器
            server_ws = ws.connect_to_server()

            # 监听来自页面（客户端）的消息
            def on_page_message(message):
                # 将页面消息转发给真实服务器
                msg = deserialize_msg_from_ws_v1(message)
                print(f"[PAGE -> SERVER]: {msg}")
                server_ws.send(message)

            # 监听来自真实服务器的消息
            def on_server_message(message):
                if isinstance(message, bytes):
                    msg = deserialize_msg_from_ws_v1(message)
                else:
                    msg = deserialize_msg_from_ws_default(message)
                print(f"[SERVER -> PAGE]: {msg}")
                ws.send(message)

            # 绑定消息监听器
            ws.on_message(on_page_message)
            server_ws.on_message(on_server_message)

            # ========== 新增：复用 server_ws 主动发送请求 ==========
            async def send_active_request():
                # 等待连接建立（可选，确保 server_ws 已就绪）
                await asyncio.sleep(1)

                # 构造 Jupyter 协议消息（示例：执行代码）
                session_id = str(uuid.uuid4())
                active_msg = {
                    "header": {
                        "msg_id": str(uuid.uuid4()),
                        "username": "python_client",
                        "session": session_id,
                        "msg_type": "execute_request",
                        "version": "5.3"
                    },
                    "parent_header": {},
                    "metadata": {},
                    "content": {
                        "code": "print('Hello from active Python client!')",
                        "silent": False,
                        "store_history": True,
                        "user_expressions": {},
                        "allow_stdin": False
                    },
                    "buffers": []
                }

                print(f"[ACTIVE CLIENT -> SERVER] 主动发送请求...")
                # 复用 server_ws 发送消息
                server_ws.send(serialize_msg_to_ws_v1(active_msg, channel="shell", pack=pack))

            # 将主动发送任务作为后台协程运行，不阻塞当前的拦截逻辑
            asyncio.create_task(send_active_request())
            # ========================================================

        # 拦截匹配 URL 的 WebSocket 连接
        await page.route_web_socket("**/api/kernels/**", ws_handler)

        await page.goto("http://127.0.0.1:8888/tree?token=a323a1d856d9054d3c16a27866851db900c2d648db7926d0")
        await asyncio.sleep(10)
        await page.goto("http://127.0.0.1:8888/notebooks/Untitled.ipynb")
        await asyncio.sleep(100)
        await browser.close()


if __name__ == '__main__':
    asyncio.run(main())

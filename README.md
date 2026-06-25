# jupyter-data-fetch

从`jupyterlab`、`jupyter notebook`中抓取数据的示例。由于代码实在过于简单，所以并未打包发布

## 优点

1. 与`ksrpc`比，通用性更强，理论上全平台通用
2. 不需中转服务器，网页能打开就能使用

## 缺点

1. `ksrpc`传输是二进制，而本项目编码成了`base85/base64`,速度较慢
2. 传输带宽消耗多，`base64`多占33%，`base85`多占25%

## 安装

1. 将`codec.py`复制到自己的项目中
2. `uv pip install -r requirements.txt`，其中关键的是`uv pip install jupyter_kernel_client`库

## 使用方法

1. `examples`下提供了示例
2. 以`joinquant`为例，打开浏览器，登录研究环境，按`F12`打开开发者工具
3. 搜索`kernels`，复制`请求URL`和`Cookie`
   ![devtool.png](docs/devtool.png)
4. 替换示例中`Cookie`和`server_url`即可
   ![ide.png](docs/ide.png)
5. 留意:`server_url`只复制一段。`Cookie`要完整复制

## 最简示例

```python
from jupyter_kernel_client import KernelClient

from jupyter_date_fetch.codec import JupyterBase85Codec

# ... 省去部分代码。更多参考examples/joinquant.py

with KernelClient(server_url="https://www.joinquant.com/user/12345678901", token=None, headers=headers) as kernel:
    # 一定要保证缩进正确
    code = """
df = get_fundamentals(query(
        valuation, income
    ).filter(
        # 这里不能使用 in 操作, 要使用in_()函数
        valuation.code.in_(['000001.XSHE', '600000.XSHG'])
    ), date='2015-10-15')
"""
    reply = kernel.execute(JupyterBase85Codec.generate_code(code, var_name='df'))
    # print(reply)
    obj = JupyterBase85Codec.extract_decode(reply)
    print(obj)

```

## 自动登录并获取数据的完整示例

参考[examples/playwright/joinquant.py](examples/playwright/joinquant.py)

## 核心代码

1. `JupyterBase85Codec`: `base85`编解码器，使用字符串传输数据，压缩率高，但部分平台会截断长字符串
2. `JupyterImageCodec`: 图片编解码器，使用图片传输数据，`base64`编码压缩率低
3. `generate_code`生成可在`Notebook`单元格中运行的代码字符串，一定要指定需要获取的变量名`var_name`
4. `kernel.execute`在服务段执行字符串代码，返回`json`对象
5. `extract_decode`从`json`中提取数据后解码成对象

## 注意

1. 由于各平台限制，`generate_code`生成的代码可能无法运行，可以复制到`Notebook`中测试
2. `python3.6`问题太多，可以打开一个`ipynb`文件后，通过菜单更改内核为最新版
3. 可以连接到已经打开的内核，只要提供`kernel_id`参数即可。参考`ricequant.py`示例
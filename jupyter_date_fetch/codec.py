import base64
from io import BytesIO

import pandas as pd

BASE_CODE = """
# 不建议用python3.6

import base64
from io import BytesIO
import gzip
import pandas as pd

try:
    buf = BytesIO()
    pd.to_pickle({0}, buf, compression='gzip') # OSError: [Errno 9] write() on read-only GzipFile object
    buf.seek(0)
    compressed = buf.read()
except OSError:
    buf = BytesIO()
    pd.to_pickle({0}, buf)
    buf.seek(0) # ValueError: I/O operation on closed file.
    compressed = gzip.compress(buf.getvalue())
"""


class JupyterTextCodec:
    """
    ## 编码
    1. 数据先pickle序列化
    2. 使用base85编码。比base64更节省空间
    3. 通过print输出。部分平台限制了print长度，可以用图片解决

    ## 解码
    1. json中提取base85字符
    2. pickle反序列化

    """

    @staticmethod
    def generate_code(*codes, var_name='df'):
        codes_str = '\n'.join(codes)
        return f"""
{codes_str}
        
{BASE_CODE.format(var_name)}

serialized = base64.b85encode(compressed).decode('ascii')
print(serialized, end='')
"""

    @staticmethod
    def extract_from_reply(reply):
        if reply['status'] == 'error':
            error_msg = '\n'.join(reply['outputs'][0]['traceback'])
            raise RuntimeError(f"Jupyter execution error:\n{error_msg}")
        else:
            return reply['outputs'][0]['text']

    @staticmethod
    def decode(text):
        return pd.read_pickle(BytesIO(base64.b85decode(text)), compression='gzip')

    @staticmethod
    def extract_decode(reply):
        text = JupyterTextCodec.extract_from_reply(reply)
        return JupyterTextCodec.decode(text)


class JupyterImageCodec:
    """
    ## 编码
    1. 数据先pickle序列化
    2. 转换到灰度图
    3. 利用Notebook展示图片，隐含了base64编码

    ## 解码
    1. json中提取图片base64
    2. base64解码后，打开为图片
    3. 提取图片数据区
    4. pickle反序列化

    """

    @staticmethod
    def generate_code(*codes, var_name='df'):
        codes_str = '\n'.join(codes)
        return f"""
{codes_str}

{BASE_CODE.format(var_name)}

import numpy as np
from PIL import Image

side = int(np.ceil(np.sqrt(len(compressed))))
padded_data = np.pad(np.frombuffer(compressed, dtype=np.uint8),(0, side * side - len(compressed)),mode='constant')
img_array = padded_data.reshape(side, side)

img = Image.fromarray(img_array, 'L') 
img
"""

    @staticmethod
    def extract_from_reply(reply):
        if reply['status'] == 'error':
            error_msg = '\n'.join(reply['outputs'][0]['traceback'])
            raise RuntimeError(f"Jupyter execution error:\n{error_msg}")
        else:
            return reply['outputs'][0]['data']['image/png']

    @staticmethod
    def decode(b64_string):
        import numpy as np
        from PIL import Image

        img_array = np.array(Image.open(BytesIO(base64.b64decode(b64_string))))
        return pd.read_pickle(BytesIO(img_array), compression='gzip')

    @staticmethod
    def extract_decode(reply):
        b64_string = JupyterImageCodec.extract_from_reply(reply)
        return JupyterImageCodec.decode(b64_string)  # if b64_string else None


# ======================================================================================

import inspect
from enum import Enum
from functools import wraps


class CodecType(Enum):
    TEXT = JupyterTextCodec
    IMAGE = JupyterImageCodec


class LazyKernel:
    _kernel = None
    _codec_type = CodecType.TEXT

    @classmethod
    def set_kernel(cls, kernel_obj):
        cls._kernel = kernel_obj

    @classmethod
    def get_kernel(cls):
        if cls._kernel is None:
            raise RuntimeError("kernel 尚未初始化")
        return cls._kernel

    @classmethod
    def set_codec(cls, codec_type: CodecType):
        cls._codec_type = codec_type

    @classmethod
    def get_codec(cls):
        if cls._codec_type == CodecType.IMAGE:
            return JupyterImageCodec
        return JupyterTextCodec


def auto_execute(func):
    """
    1. 在Notebook中用`help(get_price)`得到函数签名，然后套装饰器
    2. 调用时必须单独一行
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        kernel = LazyKernel.get_kernel()
        codec = LazyKernel.get_codec()

        frame = inspect.currentframe().f_back
        call_line = inspect.getframeinfo(frame).code_context[0].strip()

        code = f"""
# 在外部调用时，必须单独成一行
# 部分函数拼接后有缺失时，需退回到原始写法

_ = {call_line}
"""
        reply = kernel.execute(codec.generate_code(code, var_name='_'))
        return codec.extract_decode(reply)

    return wrapper

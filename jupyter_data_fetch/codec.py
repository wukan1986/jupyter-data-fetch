import base64
from io import BytesIO
from types import SimpleNamespace

import pandas as pd

BASE_CODE = """
# 不建议用python3.6

from io import BytesIO
import pandas as pd

try:
    buf = BytesIO()
    pd.to_pickle({0}, buf, compression='gzip') # OSError: [Errno 9] write() on read-only GzipFile object
    buf.seek(0)
    compressed = buf.read()
except OSError:
    import gzip

    buf = BytesIO()
    pd.to_pickle({0}, buf)
    buf.seek(0) # ValueError: I/O operation on closed file.
    compressed = gzip.compress(buf.getvalue())
"""

TO_DICT_CODE = """
# 客户端无法反序列化的类，转换成字典
def object_to_dict(obj, exclude=None):

    exclude = set(exclude or [])
    return {
        attr: getattr(obj, attr)
        for attr in dir(obj)
        if not attr.startswith('_') 
        and attr not in exclude
        and not callable(getattr(obj, attr))
    }
"""


def dict_to_object(d, exclude=None):
    """从字典恢复为命名空间对象"""
    exclude = set(exclude or [])
    filtered = {k: v for k, v in d.items() if k not in exclude}
    return SimpleNamespace(**filtered)


def extract_from_reply(reply):
    """print和!,都是走本路径"""
    if reply['status'] == 'error':
        error_msg = '\n'.join(reply['outputs'][0]['traceback'])
        raise RuntimeError(f"Jupyter execution error:\n{error_msg}")
    else:
        return reply['outputs'][0]['text']


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

import base64

base64.b85encode(compressed).decode('ascii')
"""

    @staticmethod
    def extract_from_reply(reply):
        if reply['status'] == 'error':
            error_msg = '\n'.join(reply['outputs'][0]['traceback'])
            raise RuntimeError(f"Jupyter execution error:\n{error_msg}")
        else:
            # return reply['outputs'][0]['text']
            return reply['outputs'][0]['data']['text/plain']

    @staticmethod
    def decode(text):
        text = text[1:-1]
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
from enum import Enum


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

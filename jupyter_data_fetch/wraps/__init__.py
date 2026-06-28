# 本目录下只是演示如何封装API

import inspect
from functools import wraps

from jupyter_data_fetch.codec import LazyKernel


def auto_execute(func):
    """
    1. 在Notebook中用`help()`得到函数签名，然后套装饰器
    2. 调用时必须单独一行
    3. 建议只是临时使用，还是要使用完整版
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
        # print(code)
        reply = kernel.execute(codec.generate_code(code, var_name='_'))
        return codec.extract_decode(reply)

    return wrapper

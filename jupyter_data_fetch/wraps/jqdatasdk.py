# Notebook中可以通过help()或??获得函数签名

from jupyter_data_fetch.codec import LazyKernel, TO_DICT_CODE, dict_to_object


def get_all_securities(types=[], date=None):
    kernel = LazyKernel.get_kernel()
    codec = LazyKernel.get_codec()
    code = f"""_ = get_all_securities({repr(types)}, {repr(date)})"""
    # print(code)
    return codec.extract_decode(kernel.execute(codec.generate_code(code, var_name='_'), store_history=False))


def get_price(security, start_date=None, end_date=None, frequency='daily', fields=None, skip_paused=False, fq='pre', count=None, panel=True, fill_paused=True, round=True):
    kernel = LazyKernel.get_kernel()
    codec = LazyKernel.get_codec()
    code = f"""_ = get_price({repr(security)}, {repr(start_date)}, {repr(end_date)}, {repr(frequency)}, {repr(fields)}, {repr(skip_paused)}, {repr(fq)}, {repr(count)}, {repr(panel)}, {repr(fill_paused)}, {repr(round)})"""
    # print(code)
    return codec.extract_decode(kernel.execute(codec.generate_code(code, var_name='_'), store_history=False))


def get_security_info(code, date=None):
    kernel = LazyKernel.get_kernel()
    codec = LazyKernel.get_codec()
    code = f"""
{TO_DICT_CODE}

_ = get_security_info({repr(code)}, {repr(date)}) # ModuleNotFoundError: No module named 'jqdata'
_ = object_to_dict(_)
"""
    _ = codec.extract_decode(kernel.execute(codec.generate_code(code, var_name='_'), store_history=False))
    return dict_to_object(_)  # 字典还原成对象


def get_fundamentals(query_object: str, date=None, statDate=None):
    """注意：原函数是传的query_object，但这要将str当object,所以不能加repr"""
    kernel = LazyKernel.get_kernel()
    codec = LazyKernel.get_codec()
    code = f"""_ = get_fundamentals({query_object}, {repr(date)}, {repr(statDate)})"""
    # print(code)
    return codec.extract_decode(kernel.execute(codec.generate_code(code, var_name='_'), store_history=False))


def get_index_weights(index_id, date=None):
    kernel = LazyKernel.get_kernel()
    codec = LazyKernel.get_codec()
    code = f"""_ = get_index_weights({repr(index_id)}, {repr(date)})"""
    return codec.extract_decode(kernel.execute(codec.generate_code(code, var_name='_'), store_history=False))


def get_extras(info, security_list, start_date=None, end_date='2015-12-31', df=True, count=None):
    kernel = LazyKernel.get_kernel()
    codec = LazyKernel.get_codec()
    code = f"""_ = get_extras({repr(info)}, {repr(security_list)}, {repr(start_date)}, {repr(end_date)}, {repr(df)}, {repr(count)})"""
    return codec.extract_decode(kernel.execute(codec.generate_code(code, var_name='_'), store_history=False))


def get_industry(security, date=None):
    kernel = LazyKernel.get_kernel()
    codec = LazyKernel.get_codec()
    code = f"""_ = get_industry({repr(security)}, {repr(date)})"""
    return codec.extract_decode(kernel.execute(codec.generate_code(code, var_name='_'), store_history=False))

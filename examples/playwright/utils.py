import logging
import pathlib
import random

import pandas as pd
from loguru import logger
from playwright_stealth import Stealth
from tenacity import retry, stop_after_attempt, wait_random, before_sleep_log


def repl_sync(f_globals, f_locals, quit_on_enter: bool):
    """同步版交互

    Examples
    --------
    >>> repl_sync(globals(), locals())

    """
    while True:
        txt = input("IN>")
        if txt == "":
            if quit_on_enter:
                break
            else:
                continue
        if txt in ("quit", ":q"):
            break

        try:
            print("OUT:", eval(txt, f_globals, f_locals))
        except Exception as e:
            print(e)

    return f_globals, f_locals


async def repl_async(f_globals, f_locals, quit_on_enter: bool):
    """异步版交互

    Examples
    --------
    >>> repl_async(globals(), locals())

    """
    while True:
        txt = input("IN>")
        if txt == "":
            if quit_on_enter:
                break
            else:
                continue
        if txt in ("quit", ":q"):
            break

        func_code = f"""
async def __inner_function__(f_globals, f_locals):
    globals().update(f_locals)
    {txt}
    globals().update(locals())
"""
        try:
            exec(func_code, f_globals, f_locals)
            print("OUT:", await f_locals['__inner_function__'](f_globals, f_locals))
        except Exception as e:
            print(e)

    return f_globals, f_locals


@retry(stop=stop_after_attempt(3), wait=wait_random(10, 20), before_sleep=before_sleep_log(logger, logging.DEBUG))
async def browser_retry(browser, proxys, ua, func, *arg, **kwargs):
    path = "_".join([func.__name__, *arg]) + ".parquet"
    path = pathlib.Path(path)
    if path.exists():
        return

    proxy = random.choice(proxys)
    user_agent = ua.random
    print(proxy, user_agent)
    context = await browser.new_context(proxy=proxy, user_agent=user_agent)
    await Stealth().apply_stealth_async(context)
    page = await context.new_page()
    df: pd.DataFrame = await func(page, *arg, **kwargs)
    df.to_parquet(path, compression="zstd")
    print(df.tail(5))

import os
from datetime import datetime


class Output:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    RED = '\033[31m'
    RESET = '\033[0m'
    __one_line = False
    __with_date = True

    @staticmethod
    def red(msg):
        __class__._print(msg, __class__.RED)

    @staticmethod
    def blue(msg):
        __class__._print(msg, __class__.OKBLUE)

    @staticmethod
    def header(msg):
        __class__._print(msg, __class__.HEADER)

    @staticmethod
    def green(msg):
        __class__._print(msg, __class__.OKGREEN)

    @staticmethod
    def _print(output, color=""):
        msg = []
        if __class__.__with_date:
            msg.extend([os.linesep, datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
        msg.extend([color, output, __class__.RESET])
        print(*msg, end=" " if Output.__one_line else os.linesep)

    @staticmethod
    def printed_task(pre_print: callable = "", pre_msg: callable = "", on_success_color: callable = "",
                     on_success_msg: callable = "", on_fail_color: callable = "",
                     on_fail_msg="", success_indicator: type = ""):

        def wrapper(fn):
            def func(*args, **kwargs):
                Output.__one_line = True
                if pre_print:
                    pre_print(pre_msg.title())
                    Output.__with_date = False

                res = fn(*args, **kwargs)
                if success_indicator != "":
                    has_success_match = isinstance(success_indicator, type(res)) or type(res) is success_indicator
                    if on_success_color and has_success_match:
                        on_success_color(on_success_msg.title())
                        Output.__with_date = False
                    elif on_fail_color and not has_success_match:
                        on_fail_color(on_fail_msg.title())
                Output.__one_line = False
                Output.__with_date = True
                return res

            return func

        return wrapper

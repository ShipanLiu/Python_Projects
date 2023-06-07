#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    # 项目的 名称是 django3， 不要修改。 假如修改项目名称的话， 这里 也要修改
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django3.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


# 会执行 main 方法
# __name__ 是当前模块名，当模块被直接运行时模块名为 __main__ ， 当模块被导入的时候， 模块名保持"__name__"不变。 这句话的意思就是，当模块被直接运行时，以下代码块将被运行，当模块是被导入时，代码块不被运行
if __name__ == '__main__':
    main()

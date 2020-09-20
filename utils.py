import time
import logging

logger = logging.getLogger()


def get_time():
    """
    获取时间
    :return:
    """
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


def get_suffix(file_name):
    """
    获取文件后缀名
    :param file_name:
    :return:
    """
    return file_name[file_name.rfind('.'):]


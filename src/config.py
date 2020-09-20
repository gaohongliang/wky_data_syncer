import configparser
import os
import logging
import sys
from src.const import Const

"""
基础读取配置文件
-read(filename)                     直接读取文件内容
-sections()                         得到所有的section，并以列表的形式返回
-options(section)                   得到该section的所有option
-items(section)                     得到该section的所有键值对
-get(section,option)                得到section中option的值，返回为string类型
-getint(section,option)             得到section中option的值，返回为int类型，还有相应的getboolean()和getfloat() 函数。

基础写入配置文件
-write(fp)                          将config对象写入至某个 .init 格式的文件  Write an .ini-format representation of the configuration state.
-add_section(section)               添加一个新的section
-set( section, option, value        对section中的option进行设置，需要调用write将内容写入配置文件 ConfigParser2
-remove_section(section)            删除某个 section
-remove_option(section, option)     删除某个 section 下的 option
"""
# 实例化
cf = configparser.ConfigParser()
"""
os.path.abspath(path)               返回path规范化的绝对路径。
os.path.split(path)                 将path分割成目录和文件名二元组返回。 
os.path.dirname(path)               返回path的目录。其实就是os.path.split(path)的第一个元素。
os.path.basename(path)              返回path最后的文件名。如何path以'／'或'\' 结尾，那么就会返回空值。即os.path.split(path)的第二个元素。
os.path.commonprefix(list)          返回list中，所有path共有的最长的路径
os.path.exists(path)                如果path存在，返回True；如果path不存在，返回False。
os.path.isabs(path)                 如果path是绝对路径，返回True。
os.path.isfile(path)                如果path是一个存在的文件，返回True。否则返回False。
os.path.isdir(path)                 如果path是一个存在的目录，则返回True。否则返回False。
os.path.join(path1[, path2[, ...]]) 将多个路径组合后返回，第一个绝对路径之前的参数将被忽略。
os.path.normcase(path)              在Linux和Mac平台上，该函数会原样返回path，在windows平台上会将路径中所有字符转换为小写，并将所有斜杠转换为饭斜杠。  
os.path.normpath(path)              规范化路径。
"""
# 获取当前的绝对路径
current_path = os.path.abspath(__file__)
# print(current_path)
# 当前文件的目录
now_cig = os.path.dirname(current_path)
# 拼接配置文件路径
con_cig = os.path.join(now_cig + "/conf/config.ini")
# 读取配置文件
cf.read(con_cig)


# 打印配置文件里面section名为"global"里面的potions
# print(cf.options(section='global'))
# 打印配置文件里面section里面的某个potions的value
# print(cf.get('global', 'delete_source_file'))


# 加添section
# cf.add_section('cc')
# 设置指定section的key=value
# cf.set('cc', 'aa', 'bb')
# print(cf.options(section='cc'))

def get_str(section, key):
    """
    根据section和key获取配置文件值
    :param section:
    :param key:
    :return:
    """
    return cf.get(section, key)


def get_int(section, key):
    """
    获取int值
    :param section:
    :param key:
    :return:
    """
    return cf.getint(section, key)


const = Const()
"""GLOBAL"""
const.GLOBAL_DELETE_SOURCE_FILE = get_int('global', 'delete_source_file') == 1
const.GLOBAL_INTERVAL = get_int('global', 'interval')
const.GLOBAL_LOGLEVEL = get_str('global', 'log_level')
const.GLOBAL_IGNORE = get_str('global', 'ignore').split(",")
const.GLOBAL_NAME_REPLACE = get_str('global', 'name_replace').split(",")
const.GLOBAL_VIDEO_SUFFIX = get_str('global', 'video_suffix').split(",")
"""SAMBA"""
const.SAMBA_HOST = get_str('samba', 'host')
const.SAMBA_PORT = get_int('samba', 'port')
const.SAMBA_USERNAME = get_str('samba', 'username')
const.SAMBA_PASSWORD = get_str('samba', 'password')
const.SAMBA_SERVICE_NAME = get_str('samba', 'service_name')
const.SAMBA_PATH = get_str('samba', 'path')
"""STORE"""
const.STORE_PATH = get_str("store", "path")

logging.basicConfig(level=const.GLOBAL_LOGLEVEL, stream=sys.stdout,
                    format='%(asctime)s - %(thread)d - %(levelname)s - %(message)s')

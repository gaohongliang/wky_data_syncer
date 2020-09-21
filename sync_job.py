from smb_client import SMBClient
from utils import logger, get_suffix
from config import const
import os, stat

JOB_IS_RUNNING = False


def is_dir_download_finish(client, path):
    """
    判断目录是否下载完成
    判断文件后缀为xltd即未下载完
    :param client:
    :param path:
    :return:
    """
    file_list = client.all_file_names_in_dir(const.SAMBA_SERVICE_NAME, path)
    is_finish = True
    for file_name in file_list:
        is_dir = client.is_directory(const.SAMBA_SERVICE_NAME, path + "/" + file_name)
        if is_dir:
            if not is_dir_download_finish(client, path + "/" + file_name):
                is_finish = False
        else:
            if not is_file_download_finish(file_name):
                is_finish = False
    return is_finish


def is_file_download_finish(file_name):
    """
    判断文件是否下载完
    判断文件后缀为xltd即未下载完
    :param file_name:
    :return:
    """
    return not file_name.endswith('.xltd')


def is_skip(file_name):
    """
    根据文件名判断是否忽略
    :param file_name:
    :return:
    """
    return get_suffix(file_name) in const.GLOBAL_IGNORE


def is_torrent(file_name):
    """
    是否为bt种子文件
    :param file_name:
    :return:
    """
    return get_suffix(file_name) == '.torrent'


def get_new_name(file_name, is_dir):
    """
    去掉名字中广告字符
    :param file_name:
    :param is_dir:
    :return:
    """
    new_name = file_name
    for r_str in const.GLOBAL_NAME_REPLACE:
        new_name = new_name.replace(r_str, '')
    if is_dir:
        suffix = get_suffix(file_name)
        if suffix in const.GLOBAL_VIDEO_SUFFIX:
            new_name = new_name.replace(suffix, "")

    return new_name


def del_smb_files(client, file_path):
    """
    递归删除文件
    """
    is_dir = client.is_directory(const.SAMBA_SERVICE_NAME, file_path)
    if is_dir:
        client.del_file(const.SAMBA_SERVICE_NAME, file_path + "/*")
        file_list = client.all_file_names_in_dir(const.SAMBA_SERVICE_NAME, file_path)
        for file_name in file_list:
            del_smb_files(client, file_path + "/" + file_name)
        client.del_dir(const.SAMBA_SERVICE_NAME, file_path)
    else:
        client.del_file(const.SAMBA_SERVICE_NAME, file_path)


def download_smb_files(client, smb_file_path, smb_file_name, is_dir, local_file_path):
    """
    下载文件
    文件夹递归处理
    """
    if is_dir:
        sub_file_list = client.all_file_names_in_dir(const.SAMBA_SERVICE_NAME,
                                                     smb_file_path + "/" + smb_file_name)
        for sub_file_name in sub_file_list:
            sub_is_dir = client.is_directory(const.SAMBA_SERVICE_NAME,
                                             smb_file_path + "/" + smb_file_name + "/" + sub_file_name)

            if sub_is_dir:
                os.mkdir(local_file_path + "/" + sub_file_name)
                os.chmod(local_file_path + "/" + sub_file_name, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
                download_smb_files(client, smb_file_path + "/" + smb_file_name, sub_file_name, sub_is_dir,
                                   local_file_path + "/" + sub_file_name)
            else:
                new_name = get_new_name(sub_file_name, False)
                from_path = smb_file_path + "/" + smb_file_name + "/" + sub_file_name
                to_path = local_file_path + "/" + new_name
                logger.info('copy [%s] to local [%s] ...' % (from_path, to_path))
                client.download(const.SAMBA_SERVICE_NAME, from_path, to_path + ".sync")
                os.rename(to_path + ".sync", to_path)
                os.chmod(to_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
                logger.info('copy ok')
    else:
        new_name = get_new_name(smb_file_name, False)
        from_path = smb_file_path + "/" + smb_file_name
        to_path = local_file_path + "/" + new_name
        logger.info('copy [%s] to local [%s] ...' % (from_path, to_path))
        client.download(const.SAMBA_SERVICE_NAME, from_path, to_path + ".sync")
        os.rename(to_path + ".sync", to_path)
        os.chmod(to_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
        logger.info('copy ok')


def job():
    """
    定时任务
    :return:
    """
    global JOB_IS_RUNNING
    if JOB_IS_RUNNING:
        logger.info("job is running,skip this time.")
        return

    JOB_IS_RUNNING = True

    client = None
    try:
        """创建连接"""
        logger.info("create smb connection.")
        client = SMBClient(const.SAMBA_USERNAME, const.SAMBA_PASSWORD, const.SAMBA_HOST, const.SAMBA_PORT)
        client.connect()

        """遍历目录"""
        logger.info("list folder files.")
        torrent_file_list = list()
        all_download_finish = True
        file_list = client.all_file_names_in_dir(const.SAMBA_SERVICE_NAME, const.SAMBA_PATH)
        for file_name in file_list:
            logger.info('sync file [%s].' % file_name)
            """忽略bt种子文件"""
            if is_torrent(file_name):
                logger.info('skip torrent file.')
                torrent_file_list.append(file_name)
                continue
                
            """根据后缀判断是否忽略跳过"""
            if is_skip(file_name):
                logger.info('ignore by name.')
                continue

            """判断是否为文件夹"""
            is_dir = client.is_directory(const.SAMBA_SERVICE_NAME, const.SAMBA_PATH + "/" + file_name)
            logger.info('file is dir : %s.' % is_dir)
            is_download_finish = False
            """判断是否有未下载完文件"""
            if is_dir:
                is_download_finish = is_dir_download_finish(client, const.SAMBA_PATH + "/" + file_name)
            else:
                is_download_finish = is_file_download_finish(const.SAMBA_PATH + "/" + file_name)
            logger.info('is wky download finish: %s.' % is_download_finish)
            if not is_download_finish:
                logger.info("didn't download finish,skip this file.")
                all_download_finish = False
                continue
            """开始下载"""
            new_dir_name = get_new_name(file_name, True)
            logger.info('new dir name:%s.' % new_dir_name)
            if os.path.exists(const.STORE_PATH + "/" + new_dir_name):
                logger.info('local file dir exists,skip this file.')
                continue
            os.mkdir(const.STORE_PATH + "/" + new_dir_name)
            os.chmod(const.STORE_PATH + "/" + new_dir_name, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

            download_smb_files(client, const.SAMBA_PATH, file_name, is_dir, const.STORE_PATH + "/" + new_dir_name)

            """删除smb文件"""
            if const.GLOBAL_DELETE_SOURCE_FILE:
                del_path = const.SAMBA_PATH + "/" + file_name
                logger.info('delete smb file or dir :%s' % del_path)
                del_smb_files(client, del_path)
                logger.info('delete smb file or dir ok')
        """没有下载中任务时删除没用的bt种子文件"""
        if all_download_finish:
            for torrent_file in torrent_file_list:
                logger.info('delete smb torrent file:%s' % torrent_file)
                del_smb_files(client, const.SAMBA_PATH + "/" + torrent_file)
    finally:
        """关闭连接"""
        logger.info("disconnect smb.")
        client.disconnect()
        JOB_IS_RUNNING = False
    """
        0 获取连接
        1 遍历目录
        2 判断是否为文件夹
            2-1 判断文件夹内文件是否下载完成，没完成忽略
            2-2 处理文件夹名，在本地创建文件夹
            2-3 初始化同步记录文件
            2-4 开始同步文件
        3 不是文件夹要判断是否下载完成
        4 在本地创建文件夹
        5 把文件同步值本地文件夹内
        6 删除smb中文件
        # 7 删除本地同步记录文件
        7 下载完自动删除

        feature
        
        智能分析文件名
        下载电影封皮、字幕
        """


if __name__ == '__main__':
    job()

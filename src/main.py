from src.config import const
from apscheduler.schedulers.blocking import BlockingScheduler
from src.sync_job import job
from src.utils import logger


def init_job():
    """
    初始化job
    :return:
    """
    # 该示例代码生成了一个BlockingScheduler调度器，使用了默认的任务存储MemoryJobStore，以及默认的执行器ThreadPoolExecutor，并且最大线程数为10。
    # BlockingScheduler：在进程中运行单个任务，调度器是唯一运行的东西
    scheduler = BlockingScheduler()
    # 采用阻塞的方式
    # 采用固定时间间隔（interval）的方式，每隔5秒钟执行一次
    scheduler.add_job(job, 'interval', seconds=const.GLOBAL_INTERVAL)
    scheduler.start()
    logger.info('data sync start ok,interval=%s' % const.GLOBAL_INTERVAL)


if __name__ == '__main__':
    logger.info('data sync start')
    init_job()
    logger.info('data sync start ok,interval=%s' % const.GLOBAL_INTERVAL)
    # conn = SMBConnection(const.SAMBA_USERNAME, const.SAMBA_PASSWORD, "", "", use_ntlm_v2=True)
    # result = conn.connect(const.SAMBA_HOST, const.SAMBA_PORT)
    # status = conn.auth_result
    #
    # print('smb connect is ok :%s' % result)
    # print('smb auth is ok :%s' % status)
    #
    # # shares = conn.listShares()
    # # print(shares)
    # # for s in shares:
    # #     print(s.name)
    #
    # # for e in conn.listPath(const.SAMBA_SERVICE_NAME, const.SAMBA_PATH):
    # #     if e.filename[0] != '.':
    # #         print(e.filename)
    #
    # fileAttr = conn.getAttributes(const.SAMBA_SERVICE_NAME, const.SAMBA_PATH + "/gh-pages.zip")
    # # print(fileAttr)
    # # print(fileAttr.create_time)
    # # print(fileAttr.last_access_time)
    # # print(fileAttr.last_write_time)
    # # print(fileAttr.last_attr_change_time)
    # # print(fileAttr.file_size)
    # # print(fileAttr.alloc_size)
    # # print(fileAttr.file_attributes)
    # # print(fileAttr.short_name)
    # # print(fileAttr.filename)
    # # print(fileAttr.file_id)
    #
    # # print()
    # # print(fileAttr.isDirectory)
    # file_size = fileAttr.file_size
    #
    # # offset = 0
    # # buffer = 1024
    # # print("file_size:%s" % file_size)
    # localFile = open(const.STORE_PATH + "/gh-pages.zip", "wb")
    # conn.retrieveFile(const.SAMBA_SERVICE_NAME, const.SAMBA_PATH + "/gh-pages.zip", localFile)
    # # while offset < file_size:
    # #     read_len = buffer
    # #     if offset + buffer > file_size:
    # #         read_len = file_size - offset
    # #     print('offset:%s' % offset)
    # #     print('read_len:%s' % read_len)
    # #     offset += read_len
    # #     conn.retrieveFileFromOffset(const.SAMBA_SERVICE_NAME, const.SAMBA_PATH + "/gh-pages.zip", localFile, offset,
    # #                                 read_len)
    # localFile.close()
    # conn.close()
    # print("download finished")

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
    7 删除本地同步记录文件
    
    feature
    解析smb 种子文件，下载完自动删除
    智能分析文件名
    下载电影封皮、字幕
    """

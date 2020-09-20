# wky_data_syncer
老母鸡下载文件自动同步工具。将老母鸡下载的文件同步到本地目录。<br>
### 实现原理
python定时任务登陆smb遍历文件列表，如果存在.xltd后缀（还未下载完）忽略，下载完的下载到本地目录，然后删除smb上的文件，下载前重新定义本地文件名去除广告字符

# 配置文件说明 /app/conf/config.ini
```text
[global]
#同步完后删除玩客云源文件
delete_source_file = 1
#定时器间隔时间 单位秒
interval = 10
#日志级别
log_level = INFO
#遍历文件时忽略的文件后缀
ignore=.torrent
#复制文件时去掉文件名中的字符串
name_replace=xxx电影,www.xxxx.com.
#视频文件格式
video_suffix=.avi,.mpeg,.mpg,.dat,.ra,.rm,.rmvb,.mov,.qt,.asf,.wmv,.mp4,.mkv
[samba]
#玩客云smb信息
host = 10.0.0.4
port = 139
username = ""
password = ""
service_name = 23ab
path = onecloud/tddownload
[store]
#本地存储目录
path = /app/store
```

# docker 运行说明
```
docker run --name wky_data_syncer \
--restart always \
-v /localdir/config.ini:/app/conf/config.ini \
-v /localdir/share:/app/store \
-d gaohongliang/wky_data_syncer
```

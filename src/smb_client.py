from smb.SMBConnection import *


class SMBClient(object):
    """
    smb连接客户端
    """
    username = ''
    password = ''
    ip = ''
    port = None

    status = False
    samba = None

    def __init__(self, username, password, ip, port=139):
        self.username = username
        self.password = password
        self.ip = ip
        self.port = port

    def connect(self):
        try:
            self.samba = SMBConnection(self.username, self.password, '', '', use_ntlm_v2=True)
            self.samba.connect(self.ip, self.port)
            self.status = self.samba.auth_result

        except:
            self.samba.close()

    def disconnect(self):
        if self.status:
            self.samba.close()

    def all_file_names_in_dir(self, service_name, dir_name):
        """
        列出文件夹内所有文件名
        :param service_name:
        :param dir_name:
        :return:
        """
        f_names = list()
        for e in self.samba.listPath(service_name, dir_name):
            # if len(e.filename) > 3: （会返回一些.的文件，需要过滤）
            if e.filename[0] != '.':
                f_names.append(e.filename)

        return f_names

    def download(self, service_name, smb_file_path, local_file_path):
        """
        下载文件
        :param service_name:服务名（smb中的文件夹名）
        :param smb_file_path: smb文件
        :param local_file_path: 本地文件
        :return:
        """
        f = open(local_file_path, 'wb')
        self.samba.retrieveFile(service_name, smb_file_path, f)
        f.close()

    # def download(self, f_names, service_name, smb_dir, local_dir):
    #     """
    #     下载文件
    #     :param f_names:文件名
    #     :param service_name:服务名（smb中的文件夹名）
    #     :param smb_dir: smb文件夹
    #     :param local_dir: 本地文件夹
    #     :return:
    #     """
    #     assert isinstance(f_names, list)
    #     for f_name in f_names:
    #         f = open(os.path.join(local_dir, f_name), 'w')
    #         self.samba.retrieveFile(service_name, os.path.join(smb_dir, f_name), f)
    #         f.close()

    def upload(self, service_name, smb_dir, file_name):
        """
        上传文件
        :param service_name:服务名（smb中的文件夹名）
        :param smb_dir: smb文件夹
        :param file_name: 本地文件夹
        :return:
        """
        self.samba.storeFile(service_name, smb_dir, file_name)

    def create_dir(self, service_name, path):
        """
        创建文件夹
        :param service_name:
        :param path:
        :return:
        """
        try:
            self.samba.createDirectory(service_name, path)

        except OperationFailure:
            pass

    def file_size(self, service_name, path):
        """
        文件大小
        :param service_name:
        :param path:
        :return:
        """
        return self.samba.getAttributes(service_name, path).file_size

    def is_directory(self, service_name, path):
        """
        判断是否为文件夹
        :param service_name:
        :param path:
        :return:
        """
        return self.samba.getAttributes(service_name, path).isDirectory

    def retrieve_file(self, service_name, path, local_file):
        """
        下载文件
        :param service_name:
        :param path:
        :param local_file:
        :return:
        """
        file_attr, file_size = self.samba.retrieveFile(service_name, path, local_file)
        return file_attr, file_size

    def retrieve_file_from_offset(self, service_name, path, offset, max_length, local_file):
        """
        断点续传下载文件
        :param service_name:
        :param path:
        :param offset:
        :param max_length:
        :param local_file:
        :return:
        """
        file_attr, file_size = self.samba.retrieveFileFromOffset(service_name, path, local_file, offset, max_length)
        return file_attr, file_size

    def del_dir(self, service_name, dir_path):
        """
        删除smb文件夹
        :param service_name:
        :param dir_path:
        :return:
        """
        self.samba.deleteDirectory(service_name, dir_path)

    def del_file(self, service_name, file_path):
        """
        删除文件
        :param service_name:
        :param file_path:
        :return:
        """
        self.samba.deleteFiles(service_name, file_path)

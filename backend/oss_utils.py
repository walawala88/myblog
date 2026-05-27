import oss2
import os
from datetime import datetime
from config import Config


class OSSStorage:
    def __init__(self):
        self.access_key_id = Config.OSS_ACCESS_KEY_ID
        self.access_key_secret = Config.OSS_ACCESS_KEY_SECRET
        self.endpoint = Config.OSS_ENDPOINT
        self.bucket_name = Config.OSS_BUCKET_NAME
        
        # 初始化认证对象
        auth = oss2.Auth(self.access_key_id, self.access_key_secret)
        # 初始化Bucket对象
        self.bucket = oss2.Bucket(auth, self.endpoint, self.bucket_name)
    
    def upload_file(self, file_stream, filename, folder='uploads'):
        """
        上传文件到OSS
        :param file_stream: 文件流
        :param filename: 原始文件名
        :param folder: OSS中的文件夹路径
        :return: 文件的OSS URL
        """
        # 生成唯一的文件名
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        unique_filename = f"{timestamp}_{filename}"
        
        # OSS中的完整路径
        oss_path = f"{folder}/{unique_filename}"
        
        try:
            # 上传文件
            result = self.bucket.put_object(oss_path, file_stream)
            
            if result.status == 200:
                # 返回文件的访问URL
                url = f"https://{self.bucket_name}.{self.endpoint}/{oss_path}"
                return url
            else:
                raise Exception(f"Upload failed with status: {result.status}")
        except Exception as e:
            print(f"OSS upload error: {str(e)}")
            raise e
    
    def delete_file(self, file_url):
        """
        从OSS删除文件
        :param file_url: 文件的OSS URL
        :return: 是否删除成功
        """
        try:
            # 从URL中提取OSS路径
            prefix = f"https://{self.bucket_name}.{self.endpoint}/"
            if file_url.startswith(prefix):
                oss_path = file_url[len(prefix):]
                self.bucket.delete_object(oss_path)
                return True
            return False
        except Exception as e:
            print(f"OSS delete error: {str(e)}")
            return False
    
    def get_file_url(self, oss_path):
        """
        获取文件的访问URL
        :param oss_path: OSS中的文件路径
        :return: 文件的访问URL
        """
        return f"https://{self.bucket_name}.{self.endpoint}/{oss_path}"


# 创建全局实例
oss_storage = OSSStorage()

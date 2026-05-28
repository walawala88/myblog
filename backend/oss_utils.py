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
        self.bucket = None
        
        # 只有配置有效时才初始化Bucket
        if self._is_config_valid():
            try:
                auth = oss2.Auth(self.access_key_id, self.access_key_secret)
                self.bucket = oss2.Bucket(auth, self.endpoint, self.bucket_name)
            except Exception as e:
                print(f"OSS init error: {str(e)}")
                self.bucket = None
    
    def _is_config_valid(self):
        """检查OSS配置是否有效"""
        return all([
            self.access_key_id,
            self.access_key_secret,
            self.bucket_name,
            self.endpoint
        ])
    
    def upload_file(self, file_stream, filename, folder='uploads'):
        """
        上传文件到OSS
        :param file_stream: 文件流
        :param filename: 原始文件名
        :param folder: OSS中的文件夹路径
        :return: 文件的OSS URL，失败返回None
        """
        if not self.bucket:
            print("OSS not configured, skipping upload")
            return None
        
        try:
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
            unique_filename = f"{timestamp}_{filename}"
            oss_path = f"{folder}/{unique_filename}"
            
            result = self.bucket.put_object(oss_path, file_stream)
            
            if result.status == 200:
                url = f"https://{self.bucket_name}.{self.endpoint}/{oss_path}"
                return url
            else:
                print(f"Upload failed with status: {result.status}")
                return None
        except Exception as e:
            print(f"OSS upload error: {str(e)}")
            return None
    
    def delete_file(self, file_url):
        """
        从OSS删除文件
        :param file_url: 文件的OSS URL
        :return: 是否删除成功
        """
        if not self.bucket:
            return False
        
        try:
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
        if not self._is_config_valid():
            return None
        return f"https://{self.bucket_name}.{self.endpoint}/{oss_path}"


# 延迟创建实例，避免模块加载时出错
def get_oss_storage():
    return OSSStorage()

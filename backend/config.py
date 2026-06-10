import os
from dotenv import load_dotenv

load_dotenv()


def _get_database_uri():
    """根据 .env 配置构建数据库连接 URI，优先使用 MySQL，回退到 SQLite"""
    db_user = os.environ.get('DB_USER', '')
    db_password = os.environ.get('DB_PASSWORD', '')
    db_host = os.environ.get('DB_HOST', '')
    db_port = os.environ.get('DB_PORT', '3306')
    db_name = os.environ.get('DB_NAME', '')

    if all([db_user, db_password, db_host, db_name]):
        return f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?charset=utf8mb4'

    # 回退到 SQLite（本地开发）
    return 'sqlite:///' + os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app.db')


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'

    SQLALCHEMY_DATABASE_URI = _get_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-here'

    # 本地文件存储目录（仅当 USE_CLOUD_STORAGE=False 时使用）
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    MUSIC_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'music_uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mp3', 'wav', 'flac', 'aac'}

    # 阿里云 OSS 云存储配置
    USE_CLOUD_STORAGE = os.environ.get('USE_CLOUD_STORAGE', 'false').lower() == 'true'
    OSS_ACCESS_KEY_ID = os.environ.get('OSS_ACCESS_KEY_ID', '')
    OSS_ACCESS_KEY_SECRET = os.environ.get('OSS_ACCESS_KEY_SECRET', '')
    OSS_BUCKET_NAME = os.environ.get('OSS_BUCKET_NAME', '')
    OSS_ENDPOINT = os.environ.get('OSS_ENDPOINT', '')

    # OSS 访问域名（用于拼接完整 URL）
    @property
    def OSS_BASE_URL(self):
        if self.USE_CLOUD_STORAGE and self.OSS_BUCKET_NAME and self.OSS_ENDPOINT:
            return f'https://{self.OSS_BUCKET_NAME}.{self.OSS_ENDPOINT}'
        return ''

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    if not os.path.exists(MUSIC_FOLDER):
        os.makedirs(MUSIC_FOLDER)

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

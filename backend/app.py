from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import config

# 👇 新增：导入OSS依赖
import oss2
import uuid
import os

app = Flask(__name__)
app.config.from_object(config['default'])

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
CORS(app)

# =======================
# 👇 新增：OSS 上传工具函数
# =======================
def upload_to_oss(file, folder="uploads"):
    """
    上传文件到阿里云OSS
    :param file: 前端上传的文件
    :param folder: 存储文件夹
    :return: 可直接访问的图片URL
    """
    try:
        # 初始化OSS认证
        auth = oss2.Auth(
            app.config['OSS_ACCESS_KEY_ID'],
            app.config['OSS_ACCESS_KEY_SECRET']
        )
        bucket = oss2.Bucket(
            auth,
            app.config['OSS_ENDPOINT'],
            app.config['OSS_BUCKET_NAME']
        )

        # 生成唯一文件名，防止覆盖
        ext = os.path.splitext(file.filename)[1]
        filename = f"{folder}/{uuid.uuid4().hex}{ext}"

        # 上传文件
        bucket.put_object(filename, file)

        # 返回OSS在线访问地址
        return f"https://{app.config['OSS_BUCKET_NAME']}.{app.config['OSS_ENDPOINT']}/{filename}"
    
    except Exception as e:
        print(f"OSS上传失败: {str(e)}")
        return None

# =======================
# 👇 新增：通用上传接口（你的博客直接用）
# =======================
@app.route('/api/upload', methods=['POST'])
def upload_file():
    # 检查是否有文件
    if 'file' not in request.files:
        return jsonify({"error": "请选择文件"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "未选择文件"}), 400

    # 上传到OSS
    file_url = upload_to_oss(file)

    if file_url:
        return jsonify({
            "url": file_url,
            "message": "上传成功"
        })
    else:
        return jsonify({"error": "上传失败"}), 500

# 导入路由（保持不变）
from routes import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
# MyBlog 宝塔面板部署指南

## 📋 目录

1. [项目环境要求](#1-项目环境要求)
2. [上传项目文件](#2-上传项目文件)
3. [一键部署脚本](#3-一键部署脚本)
4. [手动部署步骤](#4-手动部署步骤)
5. [端口放行说明](#5-端口放行说明)
6. [Nginx 配置指南](#6-nginx-配置指南)
7. [常见问题排查](#7-常见问题排查)

---

## 1. 项目环境要求

| 组件 | 版本 | 说明 |
|------|------|------|
| **Python** | 3.10+ | 后端运行环境 |
| **Node.js** | 18.x+ | 前端构建工具 |
| **Nginx** | 1.22+ | Web 服务器 / 反向代理 |
| **MySQL** | 8.0+ | 可选，默认使用 SQLite |
| **pip** | 21+ | Python 包管理器 |
| **npm** | 9+ | Node 包管理器 |

### 技术栈

```
后端: Flask 3.1 + SQLAlchemy + JWT + CORS + Bcrypt
前端: Vue 3 + Vue Router + Vite + Axios + SCSS
数据库: SQLite (默认) / MySQL (可选)
存储: 本地文件系统 / 阿里云 OSS (可选)
```

### Python 依赖

- Flask==3.1.1
- Flask-SQLAlchemy==3.1.1
- Flask-Migrate==4.1.0
- Flask-Bcrypt==1.0.1
- Flask-JWT-Extended==4.7.1
- Flask-CORS==5.0.1
- python-dotenv==1.1.0
- PyMySQL==1.1.1
- oss2==2.19.1
- requests==2.32.3
- gunicorn==23.0.0

---

## 2. 上传项目文件

### 方式一：宝塔面板直接上传

1. 压缩项目文件（本地 `MyBlog/` 文件夹打包为 `MyBlog.zip`）
2. 宝塔面板 → 文件 → 上传到 `/www/wwwroot/`
3. 解压：`unzip MyBlog.zip -d /www/wwwroot/`
4. 重命名：`mv /www/wwwroot/MyBlog /www/wwwroot/myblog`

### 方式二：宝塔终端 wget（从 Git 仓库）

```bash
cd /www/wwwroot/
git clone https://github.com/你的账户/MyBlog.git myblog
```

### 文件结构检查

部署完成后，终端确认结构：

```bash
ls -la /www/wwwroot/myblog/
# 应看到 backend/ frontend/ deploy/ 等目录
ls -la /www/wwwroot/myblog/backend/
# 应看到 app.py config.py routes.py requirements.txt 等
ls -la /www/wwwroot/myblog/frontend/
# 应看到 package.json vite.config.js src/ 等
```

---

## 3. 一键部署脚本 ⭐（推荐）

上传项目后，在宝塔终端执行以下命令即可全自动部署：

```bash
# 1. 进入项目目录
cd /www/wwwroot/myblog

# 2. 给脚本执行权限
chmod +x deploy/deploy.sh

# 3. 运行部署脚本
./deploy/deploy.sh
```

### 脚本会自动完成：

| 步骤 | 内容 |
|------|------|
| ✅ 安装 Python3 + pip3 | 系统包管理器安装 |
| ✅ 安装 Node.js 18 | 从 NodeSource 官方源安装 |
| ✅ 安装 Nginx | 系统包管理器安装 |
| ✅ 安装 MySQL | 可选（如选择使用） |
| ✅ 创建项目目录 | 自动检测已有文件 |
| ✅ 配置 `.env` 环境变量 | 自动生成随机密钥 |
| ✅ 创建 Python 虚拟环境 | 隔离依赖 |
| ✅ 安装 Python 依赖 | requirements.txt |
| ✅ 初始化数据库 | 运行 init_db.py |
| ✅ 安装前端依赖 | npm install |
| ✅ 构建前端 | npm run build → dist/ |
| ✅ 创建 systemd 服务 | 自动重启、开机自启 |
| ✅ 配置 Nginx | 反向代理 + 静态文件 |
| ✅ 启动所有服务 | Flask + Nginx |

### 管理员初始信息

```
登录地址: http://你的域名/login
用户名:   admin
密码:     admin123
```

---

## 4. 手动部署步骤

如果一键脚本执行失败，可以按以下步骤手动操作。

### 4.1 安装系统依赖

```bash
# Ubuntu / Debian
apt update
apt install -y python3 python3-pip python3-venv python3-dev nginx
curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
apt install -y nodejs

# CentOS / Rocky / Almalinux
yum install -y python3 python3-pip python3-devel nginx
curl -fsSL https://rpm.nodesource.com/setup_18.x | bash -
yum install -y nodejs
```

### 4.2 配置后端

```bash
# 进入后端目录
cd /www/wwwroot/myblog/backend

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖（逐个安装，避免版本冲突）
pip install --upgrade pip
pip install Flask==3.1.1
pip install Flask-SQLAlchemy==3.1.1
pip install Flask-Migrate==4.1.0
pip install Flask-Bcrypt==1.0.1
pip install Flask-JWT-Extended==4.7.1
pip install Flask-CORS==5.0.1
pip install python-dotenv==1.1.0
pip install PyMySQL==1.1.1
pip install oss2
pip install requests==2.32.3
pip install gunicorn==23.0.0

# 配置环境变量
cat > .env << 'EOF'
# ========== MySQL 数据库配置 ==========
# 如果不用MySQL，注释掉以下4行即可使用SQLite
# DB_USER=root
# DB_PASSWORD=你的密码
# DB_HOST=localhost
# DB_PORT=3306
# DB_NAME=myblog

# ========== Flask 密钥 ==========
JWT_SECRET_KEY=你的随机密钥
SECRET_KEY=你的随机密钥

# ========== GLM AI 对话 API ==========
# GLM_API_KEY=你的密钥
# GLM_API_URL=https://open.bigmodel.cn/api/paas/v4/chat/completions

# ========== 阿里云 OSS 云存储配置 ==========
USE_CLOUD_STORAGE=false
EOF

# 初始化数据库
python init_db.py

# 创建上传目录
mkdir -p uploads music_uploads

# 退出虚拟环境
deactivate
```

### 4.3 构建前端

```bash
cd /www/wwwroot/myblog/frontend
npm install --legacy-peer-deps
npm run build
```

### 4.4 配置 Flask 系统服务

```bash
# 创建启动脚本
cat > /www/wwwroot/myblog/backend/start.sh << 'EOF'
#!/bin/bash
DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"
source venv/bin/activate
export FLASK_ENV=production
mkdir -p logs
exec gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 \
  --access-logfile logs/access.log \
  --error-logfile logs/error.log \
  app:app
EOF
chmod +x /www/wwwroot/myblog/backend/start.sh

# 创建 systemd 服务
cat > /etc/systemd/system/myblog.service << 'EOF'
[Unit]
Description=MyBlog Flask Application
After=network.target

[Service]
User=www
Group=www
WorkingDirectory=/www/wwwroot/myblog/backend
Environment="FLASK_ENV=production"
ExecStart=/www/wwwroot/myblog/backend/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 --access-logfile /www/wwwroot/myblog/backend/logs/access.log --error-logfile /www/wwwroot/myblog/backend/logs/error.log app:app
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# 启动服务
systemctl daemon-reload
systemctl start myblog
systemctl enable myblog

# 验证启动
systemctl status myblog
ss -tlnp | grep 5000
```

### 4.5 配置 Nginx（详见第6节）

### 4.6 启动 Nginx

```bash
nginx -t && systemctl restart nginx
```

---

## 5. 端口放行说明

### 5.1 必须放行的端口

| 端口 | 协议 | 用途 | 说明 |
|------|------|------|------|
| **80** | TCP | HTTP | 网站访问，必须放行 |
| **443** | TCP | HTTPS | 如果配置了 SSL 证书 |
| **5000** | TCP | Flask API | **仅需内网开放**，Nginx通过内网访问 |

### 5.2 阿里云安全组配置

登录阿里云控制台 → 云服务器 ECS → 安全组 → 配置规则：

```
入方向 - 添加规则：
┌──────────────┬────────┬────────────┬───────────────┐
│ 端口范围      │ 协议   │ 授权对象   │ 描述           │
├──────────────┼────────┼────────────┼───────────────┤
│ 80/80        │ TCP    │ 0.0.0.0/0  │ HTTP          │
│ 443/443      │ TCP    │ 0.0.0.0/0  │ HTTPS (可选)  │
└──────────────┴────────┴────────────┴───────────────┘
```

> ⚠️ **重要**：端口 5000（Flask）**不需要**在安全组放行！
> Nginx 通过 127.0.0.1:5000 内网地址访问 Flask，外网直接访问 80 端口即可。

### 5.3 宝塔面板安全配置

宝塔面板 → 安全 → 放行端口：

```
80     ✅ HTTP
443    ✅ HTTPS（如果使用）
```

> 宝塔面板的 5000 端口也建议**不放行**，只需内网访问。

### 5.4 防火墙配置

如果系统防火墙（firewalld 或 ufw）已启用：

```bash
# firewalld (CentOS)
firewall-cmd --permanent --add-service=http
firewall-cmd --permanent --add-service=https
firewall-cmd --reload

# ufw (Ubuntu)
ufw allow 80/tcp
ufw allow 443/tcp
```

---

## 6. Nginx 配置指南

### 6.1 宝塔面板配置方式（推荐）

1. 宝塔面板 → 网站 → 添加站点
2. 域名：填写你的域名或服务器 IP
3. 根目录：`/www/wwwroot/myblog/frontend/dist`
4. 创建后 → 设置 → 配置文件
5. 将 `deploy/myblog_nginx.conf` 的内容粘贴进去
6. 修改 `server_name`、`root` 和 `alias` 路径为你的实际值
7. 保存 → 重载配置

### 6.2 独立 Nginx 配置

复制 `deploy/myblog_nginx.conf` 到 Nginx 配置目录：

```bash
cp deploy/myblog_nginx.conf /etc/nginx/conf.d/myblog.conf
```

修改配置文件中的三个占位符：
1. `server_name` → 你的域名或服务器 IP
2. `root` → 前端 dist 目录实际路径
3. `alias` → uploads 和 music_uploads 实际路径

然后重载 Nginx：

```bash
nginx -t && nginx -s reload
```

### 6.3 Nginx 配置要点说明

```
客户端上传限制: client_max_body_size 50m;
  └─ 博客上传图片/音乐时不能太小

前端 SPA 路由: try_files $uri $uri/ /index.html;
  └─ 确保 /about /archive 等路由刷新不404

API 反向代理: /api/ → http://127.0.0.1:5000
  └─ 前端请求 /api/posts 自动转发到 Flask

静态资源缓存: expires 1d;
  └─ 浏览器缓存图片/JS/CSS 1天

安全限制: deny all for .env .git __pycache__
  └─ 防止敏感文件泄露
```

---

## 7. 常见问题排查

### Q1: 页面显示 "502 Bad Gateway"

**原因**: Nginx 无法连接到 Flask 后端

**排查**:
```bash
# 1. 检查 Flask 是否运行
ss -tlnp | grep 5000
# 有输出 → Flask 在运行
# 无输出 → Flask 未启动

# 2. 如果未启动，检查日志
tail -50 /www/wwwroot/myblog/backend/logs/error.log

# 3. 手动启动测试
cd /www/wwwroot/myblog/backend
source venv/bin/activate
python app.py
# 看是否有报错信息
```

### Q2: 页面显示 "404 Not Found"

**原因**: Nginx 静态文件路径配置错误

**排查**:
```bash
# 1. 检查前端 dist 目录是否存在
ls -la /www/wwwroot/myblog/frontend/dist/
# 应该有 index.html 和 assets/ 目录

# 2. 如果不存在，重新构建前端
cd /www/wwwroot/myblog/frontend
npm run build

# 3. 测试 Nginx 配置
nginx -t
```

### Q3: 页面显示 "500 Internal Server Error"

**原因**: Flask 后端代码报错

**排查**:
```bash
# 查看 Flask 错误日志
tail -100 /www/wwwroot/myblog/backend/logs/error.log

# 常见原因：
# 1. 数据库文件权限问题
chown -R www:www /www/wwwroot/myblog/backend/app.db
chown -R www:www /www/wwwroot/myblog/backend/uploads/
chown -R www:www /www/wwwroot/myblog/backend/music_uploads/

# 2. Python 依赖缺失
source /www/wwwroot/myblog/backend/venv/bin/activate
pip list | grep -E "Flask|SQLAlchemy|JWT"
```

### Q4: 上传图片显示为空白

**原因**: uploads 目录权限不足或 Nginx 配置错误

**排查**:
```bash
# 1. 检查权限
ls -la /www/wwwroot/myblog/backend/uploads/
chown -R www:www /www/wwwroot/myblog/backend/uploads/

# 2. 检查 Nginx 配置中的 alias 路径
cat /www/server/panel/vhost/nginx/myblog.conf | grep alias
# 确保路径末尾有 /
```

### Q5: /login 页面空白或不显示

**原因**: 前端 SPA 路由未正确配置

**排查**:
```bash
# 确保 Nginx 配置中有:
# location / { try_files $uri $uri/ /index.html; }

# 如果没有这一行，刷新非根路径时会出现空白
```

### Q6: 数据库错误 "no such table"

**原因**: 数据库未初始化

**排查**:
```bash
cd /www/wwwroot/myblog/backend
source venv/bin/activate
python init_db.py
deactivate
systemctl restart myblog
```

### Q7: "Port 5000 already in use"

**原因**: 端口被占用

**排查**:
```bash
# 查找占用端口的进程
fuser 5000/tcp
# 或
ss -tlnp | grep 5000

# 杀掉进程
fuser -k 5000/tcp

# 重新启动
systemctl restart myblog
```

### Q8: 外网无法访问

**排查步骤**:
```bash
# 1. 先测试本地能否访问
curl -I http://127.0.0.1:80          # 测试 Nginx
curl -I http://127.0.0.1:5000/api/posts  # 测试 Flask

# 2. 检查阿里云安全组（控制台操作）
# 确保入方向有 80 端口的放行规则

# 3. 检查宝塔安全
# 宝塔面板 → 安全 → 查看 80 端口是否放行

# 4. 检查系统防火墙
systemctl status firewalld  # 如果开启，确保 80 端口放行
```

---

## 📞 运维命令速查

```bash
# 后端管理
systemctl start myblog       # 启动
systemctl stop myblog        # 停止
systemctl restart myblog     # 重启
systemctl status myblog      # 状态
journalctl -u myblog -f      # 实时日志

# Nginx 管理
nginx -t                     # 测试配置
systemctl restart nginx      # 重启
systemctl reload nginx       # 热重载
tail -f /www/wwwlogs/myblog_access.log   # 访问日志
tail -f /www/wwwlogs/myblog_error.log    # 错误日志

# 后端日志
tail -f /www/wwwroot/myblog/backend/logs/access.log
tail -f /www/wwwroot/myblog/backend/logs/error.log

# 文件权限修复
chown -R www:www /www/wwwroot/myblog/
```
#!/bin/bash
# ============================================================
# MyBlog - 宝塔面板全自动部署脚本
# 用法: 在宝塔终端运行:
#   chmod +x deploy.sh && ./deploy.sh
# ============================================================

set -e

# ---------- 颜色输出 ----------
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log()  { echo -e "${GREEN}[✔]${NC} $1"; }
warn() { echo -e "${YELLOW}[!]${NC} $1"; }
err()  { echo -e "${RED}[✘]${NC} $1"; }
info() { echo -e "${BLUE}[→]${NC} $1"; }

# ---------- 配置参数（请按需修改）----------
PROJECT_DIR="/www/wwwroot/myblog"          # 项目部署路径
DOMAIN="your-domain.com"                   # 你的域名（或服务器IP）
PYTHON_CMD="python3"                       # Python 命令
NODE_CMD="node"                            # Node 命令

# MySQL 配置（如果不用MySQL请留空，自动使用SQLite）
MYSQL_DB="myblog"
MYSQL_USER="myblog"
MYSQL_PASSWORD="$(openssl rand -base64 16 | tr -dc 'a-zA-Z0-9' | head -c16)"

# Flask 密钥（自动生成）
JWT_SECRET_KEY="$(openssl rand -base64 32)"
SECRET_KEY="$(openssl rand -base64 32)"

# ---------- 前置检查 ----------
echo -e "${BLUE}============================================${NC}"
echo -e "${BLUE}    MyBlog 博客 - 宝塔自动部署脚本${NC}"
echo -e "${BLUE}============================================${NC}"
echo ""

# 检查是否以 root 运行
if [[ $EUID -ne 0 ]]; then
   warn "建议以 root 用户运行此脚本（sudo ./deploy.sh）"
   warn "部分操作可能需要 root 权限"
fi

# 检查系统包管理器
if command -v apt &> /dev/null; then
    PKG_MANAGER="apt"
elif command -v yum &> /dev/null; then
    PKG_MANAGER="yum"
else
    err "不支持的 Linux 发行版"
    exit 1
fi

info "系统包管理器: ${PKG_MANAGER}"

# ---------- 交互输入 ----------
read -p "请输入你的域名（或服务器IP，如 123.456.78.9）: " input_domain
if [ -n "$input_domain" ]; then
    DOMAIN="$input_domain"
fi

read -p "请输入项目部署路径 [${PROJECT_DIR}]: " input_dir
if [ -n "$input_dir" ]; then
    PROJECT_DIR="$input_dir"
fi

read -p "是否使用 MySQL？(y/n, 默认 n 使用 SQLite): " use_mysql
echo ""

# ============================================================
# 第一步：安装系统依赖
# ============================================================
echo -e "${YELLOW}========== 第一步：安装系统依赖 ==========${NC}"

# 检查 Python3
if ! command -v $PYTHON_CMD &> /dev/null; then
    info "安装 Python3..."
    if [ "$PKG_MANAGER" = "apt" ]; then
        apt update && apt install -y python3 python3-pip python3-venv python3-dev
    elif [ "$PKG_MANAGER" = "yum" ]; then
        yum install -y python3 python3-pip python3-devel
    fi
    log "Python3 安装完成"
else
    log "Python3 已安装: $($PYTHON_CMD --version)"
fi

# 检查 pip3
if ! command -v pip3 &> /dev/null; then
    info "安装 pip3..."
    if [ "$PKG_MANAGER" = "apt" ]; then
        apt install -y python3-pip
    elif [ "$PKG_MANAGER" = "yum" ]; then
        yum install -y python3-pip
    fi
    log "pip3 安装完成"
fi

# 检查 Node.js（前端构建需要）
if ! command -v $NODE_CMD &> /dev/null; then
    info "安装 Node.js 18..."
    if [ "$PKG_MANAGER" = "apt" ]; then
        curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
        apt install -y nodejs
    elif [ "$PKG_MANAGER" = "yum" ]; then
        curl -fsSL https://rpm.nodesource.com/setup_18.x | bash -
        yum install -y nodejs
    fi
    log "Node.js 安装完成: $($NODE_CMD --version)"
else
    log "Node.js 已安装: $($NODE_CMD --version)"
fi

# 检查 nginx
if ! command -v nginx &> /dev/null; then
    info "安装 Nginx..."
    if [ "$PKG_MANAGER" = "apt" ]; then
        apt install -y nginx
    elif [ "$PKG_MANAGER" = "yum" ]; then
        yum install -y nginx
    fi
    systemctl enable nginx
    log "Nginx 安装完成"
else
    log "Nginx 已安装: $(nginx -v 2>&1)"
fi

# 安装 MySQL 客户端库（编译依赖）
if [ "$PKG_MANAGER" = "apt" ]; then
    apt install -y default-libmysqlclient-dev build-essential pkg-config 2>/dev/null || true
elif [ "$PKG_MANAGER" = "yum" ]; then
    yum install -y mysql-devel gcc gcc-c++ 2>/dev/null || true
fi

# 检查宝塔MySQL（如果选择使用MySQL）
if [[ "$use_mysql" =~ ^[Yy]$ ]]; then
    if command -v mysql &> /dev/null; then
        log "MySQL 已安装: $(mysql --version)"
    else
        warn "未检测到 MySQL 客户端，请先在宝塔面板中安装 MySQL（建议 8.0）"
        warn "安装完成后重新运行此脚本"
        warn "或在宝塔 → 数据库 → 添加数据库，记下数据库信息后继续"
        echo ""
        read -p "MySQL 已安装好了吗？按回车继续..."
    fi
fi

echo ""

# ============================================================
# 第二步：准备项目目录
# ============================================================
echo -e "${YELLOW}========== 第二步：准备项目目录 ==========${NC}"

# 检查项目文件是否已上传
if [ ! -d "$PROJECT_DIR" ]; then
    info "创建项目目录: ${PROJECT_DIR}"
    mkdir -p "$PROJECT_DIR"
else
    log "项目目录已存在: ${PROJECT_DIR}"
fi

cd "$PROJECT_DIR"

# 检查是否有项目文件
if [ ! -f "backend/app.py" ] || [ ! -d "frontend" ]; then
    err "未检测到项目文件！"
    err "请确保："
    err "1. 在宝塔面板中上传整个 MyBlog 文件夹到 ${PROJECT_DIR}"
    err "2. 或者上传压缩包后在终端执行: unzip MyBlog.zip -d ${PROJECT_DIR}"
    err ""
    err "正确结构应该是："
    err "  ${PROJECT_DIR}/"
    err "  ├── backend/"
    err "  │   ├── app.py"
    err "  │   ├── config.py"
    err "  │   ├── requirements.txt"
    err "  │   └── ..."
    err "  ├── frontend/"
    err "  │   ├── package.json"
    err "  │   ├── vite.config.js"
    err "  │   ├── src/"
    err "  │   └── ..."
    exit 1
fi
log "项目文件检测通过"

echo ""

# ============================================================
# 第三步：配置 MySQL 数据库
# ============================================================
if [[ "$use_mysql" =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}========== 第三步：配置 MySQL 数据库 ==========${NC}"

    # 自动创建数据库和用户
    info "正在创建 MySQL 数据库 ${MYSQL_DB}..."

    # 尝试获取 MySQL root 密码
    if [ -f "/www/server/mysql/data/auto.cnf" ]; then
        MYSQL_ADMIN="root"
    fi

    # 尝试常见宝塔MySQL密码
    BT_PASSWORD=""
    if [ -f "/www/server/panel/data/default.db" ]; then
        BT_PASSWORD=$(cat /www/server/panel/data/pass.txt 2>/dev/null || echo "")
    fi

    # 创建数据库
    mysql -u root -e "CREATE DATABASE IF NOT EXISTS ${MYSQL_DB} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;" 2>/dev/null || \
    mysql -u root -p"${BT_PASSWORD}" -e "CREATE DATABASE IF NOT EXISTS ${MYSQL_DB} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;" 2>/dev/null || {
        warn "自动创建数据库失败，请手动操作："
        warn "1. 打开宝塔面板 → 数据库 → 添加数据库"
        warn "2. 数据库名: ${MYSQL_DB}"
        warn "3. 用户名: ${MYSQL_USER}"
        warn "4. 密码: ${MYSQL_PASSWORD}"
        echo ""
        read -p "数据库创建完成后，输入数据库密码（或按回车使用自动生成的密码）: " input_mysql_pass
        MYSQL_PASSWORD="${input_mysql_pass:-$MYSQL_PASSWORD}"
        read -p "输入数据库用户名 [${MYSQL_USER}]: " input_mysql_user
        MYSQL_USER="${input_mysql_user:-$MYSQL_USER}"
    }

    # 如果自动创建成功
    if [ $? -eq 0 ]; then
        mysql -u root -e "CREATE USER IF NOT EXISTS '${MYSQL_USER}'@'localhost' IDENTIFIED BY '${MYSQL_PASSWORD}';" 2>/dev/null
        mysql -u root -e "GRANT ALL PRIVILEGES ON ${MYSQL_DB}.* TO '${MYSQL_USER}'@'localhost'; FLUSH PRIVILEGES;" 2>/dev/null
        log "MySQL 数据库创建成功"
        log "  数据库: ${MYSQL_DB}"
        log "  用户名: ${MYSQL_USER}"
        log "  密码:   ${MYSQL_PASSWORD}"
    fi
    echo ""
fi

# ============================================================
# 第四步：配置后端环境
# ============================================================
echo -e "${YELLOW}========== 第四步：配置后端环境 ==========${NC}"

cd "$PROJECT_DIR/backend"

# 创建 .env 文件
info "配置 .env 环境变量文件..."

cat > .env << EOF
# ========== MySQL 数据库配置 ==========
$(if [[ "$use_mysql" =~ ^[Yy]$ ]]; then
echo "DB_USER=${MYSQL_USER}
DB_PASSWORD=${MYSQL_PASSWORD}
DB_HOST=localhost
DB_PORT=3306
DB_NAME=${MYSQL_DB}"
else
echo "# DB_USER=root
# DB_PASSWORD=your_mysql_password
# DB_HOST=localhost
# DB_PORT=3306
# DB_NAME=myblog"
fi
)

# ========== Flask 密钥 ==========
JWT_SECRET_KEY=${JWT_SECRET_KEY}
SECRET_KEY=${SECRET_KEY}

# ========== GLM AI 对话 API（如需AI功能请填写真实密钥） ==========
# GLM_API_KEY=your-glm-api-key
# GLM_API_URL=https://open.bigmodel.cn/api/paas/v4/chat/completions

# ========== 阿里云 OSS 云存储配置（如需使用请填写） ==========
USE_CLOUD_STORAGE=false
# OSS_ACCESS_KEY_ID=你的AccessKeyId
# OSS_ACCESS_KEY_SECRET=你的AccessKeySecret
# OSS_BUCKET_NAME=你的Bucket名称
# OSS_ENDPOINT=oss-cn-beijing.aliyuncs.com
EOF
log ".env 文件已创建"

# 创建 Python 虚拟环境
if [ ! -d "venv" ]; then
    info "创建 Python 虚拟环境..."
    $PYTHON_CMD -m venv venv
    log "虚拟环境创建成功"
else
    log "虚拟环境已存在"
fi

# 激活虚拟环境并安装依赖
info "安装 Python 依赖（${PROJECT_DIR}/backend/requirements.txt）..."

# 备份原始 requirements.txt
cp requirements.txt requirements.txt.bak

# 宝塔环境特殊处理：移除有问题的 oss2 版本限制，确保兼容
source venv/bin/activate

# 升级 pip
pip install --upgrade pip -q

# 优先安装编译依赖
pip install wheel setuptools -q

# 按顺序安装依赖
pip install Flask==3.1.1
pip install Flask-SQLAlchemy==3.1.1
pip install Flask-Migrate==4.1.0
pip install Flask-Bcrypt==1.0.1
pip install Flask-JWT-Extended==4.7.1
pip install Flask-CORS==5.0.1
pip install python-dotenv==1.1.0
pip install requests==2.32.3

# 如果使用 MySQL，安装 PyMySQL
if [[ "$use_mysql" =~ ^[Yy]$ ]]; then
    pip install PyMySQL==1.1.1
else
    # 仍然安装但不启用MySQL
    pip install PyMySQL==1.1.1 2>/dev/null || true
fi

# 安装 OSS 支持（可选，不影响启动）
pip install oss2==2.19.1 2>/dev/null || pip install oss2 2>/dev/null || true

# 安装生产环境 WSGI 服务器
pip install gunicorn==23.0.0

log "Python 依赖安装完成"
deactivate

# 创建必要的目录
mkdir -p uploads music_uploads
log "创建 uploads/ 和 music_uploads/ 目录"

echo ""

# ============================================================
# 第五步：初始化数据库
# ============================================================
echo -e "${YELLOW}========== 第五步：初始化数据库 ==========${NC}"

cd "$PROJECT_DIR/backend"
source venv/bin/activate

info "运行数据库初始化..."
$PYTHON_CMD init_db.py && log "数据库初始化成功" || warn "数据库初始化可能有警告，但通常是正常的"

deactivate

echo ""

# ============================================================
# 第六步：构建前端
# ============================================================
echo -e "${YELLOW}========== 第六步：构建前端 ==========${NC}"

cd "$PROJECT_DIR/frontend"

if [ ! -d "node_modules" ]; then
    info "安装前端依赖..."
    npm install --legacy-peer-deps 2>&1 | tail -5
    log "前端依赖安装完成"
else
    log "前端依赖已安装"
fi

# 修改 Vite 配置，设置生产环境 API 路径
info "配置前端构建参数..."

# 创建生产环境专属 vite 配置
cat > vite.config.js << 'VITEEOF'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': '/src'
    }
  },
  // 生产构建配置
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    // 生成相对路径，方便部署到子目录
    assetsInlineLimit: 4096,
  }
})
VITEEOF
log "Vite 生产配置已生成"

# 构建前端
info "构建前端静态文件..."
npm run build 2>&1 | tail -10
if [ -d "dist" ]; then
    log "前端构建成功！输出目录: ${PROJECT_DIR}/frontend/dist/"
else
    err "前端构建失败！"
    err "请检查 npm install 日志"
    exit 1
fi

echo ""

# ============================================================
# 第七步：配置 Gunicorn 系统服务
# ============================================================
echo -e "${YELLOW}========== 第七步：配置后端服务 ==========${NC}"

# 创建 Gunicorn 启动脚本
cat > "$PROJECT_DIR/backend/start.sh" << 'GUNICORNEOF'
#!/bin/bash
# MyBlog Flask 生产启动脚本
DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"
source venv/bin/activate

# 设置生产环境变量（覆盖 .env 中的默认配置）
export FLASK_ENV=production

# 确保日志目录存在
mkdir -p logs

# 启动 Gunicorn
# -w 4: 4个工作进程（可根据CPU核数调整）
# -b 0.0.0.0:5000: 监听所有网卡的5000端口
# --timeout 120: 超时时间120秒
# --access-logfile: 访问日志
# --error-logfile: 错误日志
exec gunicorn -w 4 \
    -b 0.0.0.0:5000 \
    --timeout 120 \
    --access-logfile logs/access.log \
    --error-logfile logs/error.log \
    app:app
GUNICORNEOF
chmod +x "$PROJECT_DIR/backend/start.sh"

# 创建 systemd 服务文件（如果不存在）
if [ ! -f "/etc/systemd/system/myblog.service" ]; then
    cat > /tmp/myblog.service << 'SYSTEMDEOF'
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
SYSTEMDEOF

    # 替换实际路径
    sed -i "s|/www/wwwroot/myblog|${PROJECT_DIR}|g" /tmp/myblog.service
    cp /tmp/myblog.service /etc/systemd/system/myblog.service
    systemctl daemon-reload
    log "系统服务 myblog.service 已创建"
else
    log "系统服务 myblog.service 已存在，跳过"
fi

echo ""

# ============================================================
# 第八步：配置 Nginx
# ============================================================
echo -e "${YELLOW}========== 第八步：配置 Nginx ==========${NC}"

# 生成 Nginx 配置
cat > /tmp/myblog_nginx.conf << NGINXEOF
# MyBlog Nginx 配置
# 将此文件放置在宝塔面板的网站配置中
# 宝塔路径: /www/server/panel/vhost/nginx/myblog.conf

server {
    listen 80;
    listen [::]:80;

    # 改成你的域名或服务器 IP
    server_name ${DOMAIN};

    # 字符集
    charset utf-8;

    # 客户端最大上传大小（用于图片/音乐上传）
    client_max_body_size 50m;

    # ========== 前端静态文件 ==========
    root ${PROJECT_DIR}/frontend/dist;
    index index.html;

    # 前端 SPA 路由：所有非文件、非API请求都返回 index.html
    location / {
        try_files \$uri \$uri/ /index.html;

        # 静态文件缓存（1天）
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
            expires 1d;
            add_header Cache-Control "public, immutable";
        }
    }

    # ========== API 反向代理到 Flask ==========
    location /api/ {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;

        # WebSocket 支持（预留）
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";

        # 超时设置
        proxy_connect_timeout 60s;
        proxy_read_timeout 60s;
        proxy_send_timeout 60s;
    }

    # ========== 本地文件上传访问 ==========
    location /uploads/ {
        alias ${PROJECT_DIR}/backend/uploads/;
        expires 7d;
        add_header Cache-Control "public, immutable";

        # 如果文件不存在，交给 Flask 处理
        try_files \$uri @flask;
    }

    location /music_uploads/ {
        alias ${PROJECT_DIR}/backend/music_uploads/;
        expires 7d;
        add_header Cache-Control "public, immutable";

        # 如果文件不存在，交给 Flask 处理
        try_files \$uri @flask;
    }

    # Flask 兜底（处理文件上传等服务端逻辑）
    location @flask {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    }

    # ========== 安全与性能 ==========
    # 禁止访问隐藏文件
    location ~ /\. {
        deny all;
        access_log off;
        log_not_found off;
    }

    # 禁止访问敏感文件
    location ~ (\.env|\.pyc|__pycache__|\.git|venv) {
        deny all;
        access_log off;
        log_not_found off;
    }

    # Gzip 压缩
    gzip on;
    gzip_min_length 1k;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/javascript application/json application/javascript application/x-javascript image/svg+xml;
    gzip_vary on;
    gzip_disable "MSIE [1-6]\.";

    # 日志
    access_log /www/wwwlogs/myblog_access.log;
    error_log /www/wwwlogs/myblog_error.log;
}
NGINXEOF

# 根据情况使用 Nginx 配置
if [ -d "/www/server/panel/vhost/nginx" ]; then
    # 宝塔面板环境
    cp /tmp/myblog_nginx.conf "/www/server/panel/vhost/nginx/myblog.conf"
    log "Nginx 配置已添加到宝塔面板"
    info "你也可以在宝塔面板中: 网站 → 添加站点 → 使用此配置"
elif [ -d "/etc/nginx/sites-available" ]; then
    # Ubuntu/Debian 标准 Nginx
    cp /tmp/myblog_nginx.conf /etc/nginx/sites-available/myblog
    ln -sf /etc/nginx/sites-available/myblog /etc/nginx/sites-enabled/
    log "Nginx 配置已添加到 sites-available"
else
    # 直接放 /etc/nginx/conf.d/
    cp /tmp/myblog_nginx.conf /etc/nginx/conf.d/myblog.conf
    log "Nginx 配置已添加到 /etc/nginx/conf.d/"
fi

echo ""

# ============================================================
# 第九步：启动服务
# ============================================================
echo -e "${YELLOW}========== 第九步：启动服务 ==========${NC}"

# 停止旧服务
info "停止旧服务..."
systemctl stop myblog 2>/dev/null || true
systemctl stop nginx 2>/dev/null || true

# 检查端口占用
if ss -tlnp | grep -q ':5000'; then
    warn "端口 5000 已被占用，正在尝试释放..."
    fuser -k 5000/tcp 2>/dev/null || true
    sleep 2
fi

# 启动后端
info "启动 Flask 后端服务..."
systemctl start myblog 2>/dev/null || {
    warn "systemd 启动失败，尝试直接启动..."
    cd "$PROJECT_DIR/backend"
    nohup ./start.sh > /dev/null 2>&1 &
}
sleep 3

# 验证后端是否启动
if ss -tlnp | grep -q ':5000'; then
    log "Flask 后端已启动 (端口 5000) ✓"
else
    warn "Flask 后端启动可能有问题，检查日志:"
    warn "  tail -50 ${PROJECT_DIR}/backend/logs/error.log"
fi

# 启动 Nginx
info "启动 Nginx..."
systemctl start nginx
systemctl enable nginx 2>/dev/null || true
log "Nginx 已启动 ✓"

# 重启 Nginx 使配置生效
nginx -t && systemctl restart nginx
log "Nginx 配置验证通过 ✓"

echo ""

# ============================================================
# 完成
# ============================================================
echo -e "${BLUE}============================================${NC}"
echo -e "${GREEN}    🎉 MyBlog 部署完成！${NC}"
echo -e "${BLUE}============================================${NC}"
echo ""
echo -e "访问地址: ${GREEN}http://${DOMAIN}${NC}"
echo ""
echo -e "${YELLOW}管理员信息:${NC}"
echo -e "  登录地址: ${GREEN}http://${DOMAIN}/login${NC}"
echo -e "  用户名:   admin"
echo -e "  密码:     admin123"
echo -e "  ${RED}⚠ 请尽快修改默认密码！${NC}"
echo ""
echo -e "${YELLOW}关键路径:${NC}"
echo -e "  项目目录:    ${PROJECT_DIR}"
echo -e "  后端日志:    tail -f ${PROJECT_DIR}/backend/logs/error.log"
echo -e "  Nginx日志:   tail -f /www/wwwlogs/myblog_error.log"
echo ""

if [[ "$use_mysql" =~ ^[Yy]$ ]]; then
echo -e "${YELLOW}MySQL 数据库信息:${NC}"
echo -e "  数据库名: ${MYSQL_DB}"
echo -e "  用户名:   ${MYSQL_USER}"
echo -e "  密码:     ${MYSQL_PASSWORD}"
fi

echo ""
echo -e "${YELLOW}管理命令:${NC}"
echo -e "  重启后端:   systemctl restart myblog"
echo -e "  查看后端:   systemctl status myblog"
echo -e "  重启Nginx:  nginx -t && systemctl restart nginx"
echo ""
echo -e "${YELLOW}如果无法访问，请检查:${NC}"
echo -e "  1. 阿里云安全组 → 放行 80 (HTTP) 和 443 (HTTPS) 端口"
echo -e "  2. 宝塔面板 → 安全 → 放行 80 和 443 端口"
echo -e "  3. 如果是域名，确认 DNS 已解析到服务器 IP"
echo -e "  4. 运行测试: ${GREEN}curl -I http://127.0.0.1${NC}"
echo ""
echo -e "${YELLOW}配置 HTTPS（强烈推荐）:${NC}"
echo -e "  宝塔面板 → 网站 → 设置 → SSL → 申请 Let's Encrypt 证书"
echo ""
echo -e "${BLUE}============================================${NC}"
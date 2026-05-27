# 个人博客系统

基于 Flask + Vue 3 构建的现代化个人博客系统，采用毛玻璃半透明UI风格。

## 功能特性

### 基础功能
- 文章发布、编辑、删除、草稿保存
- 文章分类管理
- 文章标签系统
- 首页文章列表（按发布时间自动排序）
- 文章详情阅读页
- 时间归档（按年月查看历史文章）
- 站内关键词搜索功能

### 互动留言功能
- 访客评论留言功能
- 评论回复、删除
- 文章点赞功能
- 文章浏览访问量统计
- 访客来访记录（访客足迹统计）

### 固定独立页面
- 「关于我」个人简介页面
- 网站公告页面
- 隐私协议与免责声明页面
- 独立留言板页面

### 后台管理功能
- 管理员账号登录与后台管理中心
- 网站基础设置（头像、站点名称、简介等）
- 图片上传与素材图库管理
- 账号权限管理与密码修改
- 访客数据统计与访问记录查看
- 电影管理（增删改）
- 音乐管理（增删改，支持 MP3/AAC 上传）

### 美化与拓展功能
- 浅色/深色（夜间模式）切换
- 文章置顶与热门文章推荐
- 首页轮播图（自动播放）与侧边栏挂件组件
- 个人图片相册图库（毛玻璃弹窗）
- 荣誉展示墙（毛玻璃卡片）
- 爱好页面（观影记录 + 音乐收藏）
- 背景音乐播放器（黑胶唱片样式）
- AI 助手（INTJ 人设 ZHH）

### 特色功能
- vibecoding 作品展示（粒子交互效果）
- 幕布笔记页面
- 收藏音乐与背景音乐互斥播放

## 技术栈

**后端:**
- Python 3.x
- Flask 2.x
- Flask-SQLAlchemy（数据库ORM）
- Flask-Migrate（数据库迁移）
- Flask-Bcrypt（密码加密）
- Flask-JWT-Extended（身份认证）
- Flask-CORS（跨域支持）
- MySQL（数据库）

**前端:**
- Vue 3（组合式API）
- Vue Router（路由管理）
- Lucide Vue（图标库）
- Vite（构建工具）
- SCSS（样式预处理）

## 项目结构

```
MyBlog/
├── backend/                 # Flask后端
│   ├── app.py              # 应用入口
│   ├── config.py           # 配置文件
│   ├── models.py           # 数据库模型
│   ├── routes.py           # API路由
│   ├── requirements.txt    # 依赖列表
│   ├── init_db.py          # 数据库初始化
│   ├── migrations/         # 数据库迁移
│   ├── uploads/            # 上传文件目录
│   └── music_uploads/      # 音乐文件目录
├── frontend/               # Vue前端
│   ├── src/
│   │   ├── main.js         # 入口文件
│   │   ├── App.vue         # 根组件
│   │   ├── router/         # 路由配置
│   │   ├── views/          # 页面视图
│   │   │   ├── admin/      # 后台管理页面
│   │   │   ├── Archive.vue # 时间归档
│   │   │   ├── Hobbies.vue # 爱好页面
│   │   │   └── ...
│   │   ├── components/     # 公共组件
│   │   │   ├── MusicPlayer.vue    # 背景音乐播放器
│   │   │   ├── AIAssistant.vue    # AI助手
│   │   │   └── ...
│   │   └── styles/         # 全局样式
│   ├── index.html          # HTML模板
│   ├── package.json        # 前端依赖
│   └── vite.config.js      # Vite配置
├── animated-characters-login-page-main/  # 登录页面组件
└── lv_0_20260525143810.mp4 # 背景视频
```

## 环境要求

- Python 3.8+
- Node.js 18+
- MySQL 8.0+

## 安装与运行

### 1. 后端配置

```bash
# 进入后端目录
cd backend

# 安装依赖
pip install -r requirements.txt

# 创建数据库（MySQL）
CREATE DATABASE blog_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 修改配置文件
# 编辑 config.py，修改数据库连接信息

# 初始化数据库
python init_db.py

# 数据库迁移（首次运行或新增模型时）
flask db migrate -m "initial migration"
flask db upgrade

# 启动后端服务
flask run
```

### 2. 前端配置

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 开发模式运行
npm run dev

# 生产构建
npm run build
```

### 3. 默认账号

用户名: `admin`
密码: `admin123`

## API接口

### 认证
- `POST /api/login` - 用户登录

### 文章
- `GET /api/posts` - 获取文章列表
- `GET /api/posts/<slug>` - 获取文章详情
- `POST /api/posts` - 创建文章（需登录）
- `PUT /api/posts/<id>` - 更新文章（需登录）
- `DELETE /api/posts/<id>` - 删除文章（需登录）
- `GET /api/admin/posts` - 获取所有文章（含草稿，需登录）

### 分类
- `GET /api/categories` - 获取分类列表

### 标签
- `GET /api/tags` - 获取标签列表

### 评论
- `GET /api/comments` - 获取评论列表
- `POST /api/comments` - 添加评论
- `DELETE /api/comments/<id>` - 删除评论（需登录）

### 电影
- `GET /api/movies` - 获取电影列表
- `POST /api/movies` - 添加电影（需登录，支持图片上传）
- `PUT /api/movies/<id>` - 更新电影（需登录）
- `DELETE /api/movies/<id>` - 删除电影（需登录）

### 音乐
- `GET /api/music` - 获取音乐列表
- `POST /api/music` - 添加音乐（需登录，支持 MP3/AAC 上传）
- `PUT /api/music/<id>` - 更新音乐（需登录）
- `DELETE /api/music/<id>` - 删除音乐（需登录）

### AI 助手
- `POST /api/chat` - AI 聊天接口

### 其他
- `GET /api/stats` - 获取统计数据
- `GET /api/archive` - 获取时间归档
- `GET /api/gallery` - 获取相册图片
- `GET /api/honors` - 获取荣誉列表
- `POST /api/visitor` - 记录访客访问
- `POST /api/like` - 点赞文章

## 部署说明

1. 后端使用 Gunicorn + Nginx 部署
2. 前端构建后部署到静态文件服务器
3. 配置 Nginx 反向代理
4. 配置文件上传目录权限

## 开发说明

- 前端开发服务器默认端口: 5173
- 后端开发服务器默认端口: 5000
- 前端通过 Vite 代理转发 API 请求到后端
- 音乐文件存储路径: `/music_uploads/`
- 图片文件存储路径: `/uploads/`

## 特色功能说明

### AI 助手
- 人设：ZHH，计算机科学与技术专业学生，INTJ 性格
- 特点：理性高效、逻辑清晰、注重结果

### 音乐播放器
- 背景音乐播放器：右上角黑胶唱片样式
- 收藏音乐播放器：爱好页面内的唱片播放器
- 互斥机制：背景音乐与收藏音乐不同时播放
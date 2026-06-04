# 多媒体处理平台

一个支持图片、音频和视频压缩与格式转换的全栈 Web 应用。

## 技术栈

- **前端**: Vue 3 + Vue Router + Axios + Vite
- **后端**: Python Flask + SQLite
- **媒体处理**: Pillow (图片) + FFmpeg (音频/视频)

## 功能特性

### 图片处理
- 支持格式: PNG, JPG, JPEG, WebP, GIF, BMP, TIFF
- 可调节压缩质量 (1-100)
- 格式互转

### 音频处理
- 支持格式: MP3, WAV, OGG, FLAC, AAC
- 可调节比特率 (64-320 kbps)
- 格式互转

### 视频处理
- 支持格式: MP4, AVI, MKV, WebM, MOV
- 可调节压缩质量 (CRF 0-51)
- 格式互转

## 系统要求

- Python 3.8+
- Node.js 16+
- FFmpeg (系统已安装并在 PATH 中)

## 快速开始

### 1. 安装 FFmpeg

```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Windows - 从 https://ffmpeg.org/download.html 下载
```

### 2. 启动后端

```bash
cd media-platform/backend

# 创建虚拟环境（可选）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 启动服务器
python app.py
```

后端服务将运行在 http://localhost:5000

### 3. 启动前端

```bash
cd media-platform/frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端将运行在 http://localhost:3000

### 4. 使用

打开浏览器访问 http://localhost:3000，即可使用多媒体处理平台。

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/health | 健康检查 |
| POST | /api/upload | 上传文件 |
| POST | /api/process | 处理文件（压缩/转换） |
| GET | /api/download/:filename | 下载处理后的文件 |
| GET | /api/tasks | 获取任务列表 |
| GET | /api/tasks/:id | 获取单个任务详情 |

### 上传文件

```bash
curl -X POST -F "file=@test.jpg" http://localhost:5000/api/upload
```

### 处理文件

```bash
curl -X POST http://localhost:5000/api/process \
  -H "Content-Type: application/json" \
  -d '{"stored_name": "xxx_test.jpg", "target_format": "webp", "quality": 80}'
```

## 项目结构

```
media-platform/
├── backend/
│   ├── app.py              # Flask 主应用
│   ├── config.py           # 配置文件
│   ├── database.py         # 数据库初始化
│   ├── processors.py       # 媒体处理逻辑
│   ├── requirements.txt    # Python 依赖
│   ├── uploads/            # 上传文件目录
│   └── outputs/            # 处理输出目录
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── main.js         # 入口文件
│       ├── App.vue         # 根组件
│       ├── api.js          # API 封装
│       └── pages/
│           ├── HomePage.vue   # 首页
│           ├── ImagePage.vue  # 图片处理页
│           ├── AudioPage.vue  # 音频处理页
│           ├── VideoPage.vue  # 视频处理页
│           └── TasksPage.vue  # 任务记录页
└── README.md
```

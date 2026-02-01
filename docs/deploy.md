用户想知道如何把前后端部署到数据库所在的服务器上。让我先了解一下项目的结构和配置，然后给出部署方案。

我需要查看：
1. 后端配置
2. 前端配置
3. 数据库配置
4. 项目结构

让我先读取相关文件来了解当前的配置情况。
我来帮你分析如何将前后端部署到数据库所在的服务器上。首先让我查看一下相关配置信息。
现在我已经获取了项目的基本信息。让我分析一下当前的情况：

1. **数据库服务器**: 106.15.36.199:3306 (MySQL)
2. **后端**: FastAPI + Uvicorn，当前配置为 localhost:8000
3. **前端**: Vue3 + Vite，当前配置为 localhost:5173，代理到后端 localhost:8000

用户想要将前后端都部署到数据库所在的服务器上（106.15.36.199）。

部署方案：

**方案一: 前后端分离部署 + Nginx反向代理**
- 后端部署在服务器上某个端口（如 8000）
- 前端打包为静态文件，通过 Nginx 服务
- Nginx 做反向代理，将 API 请求转发到后端

**方案二: 前后端同域部署**
- 前端打包后，将 dist 文件夹内容放到后端作为静态文件服务
- 后端 FastAPI 同时服务 API 和前端静态文件

**方案三: Docker 容器化部署**
- 使用 Docker Compose 部署前后端

让我给出详细的部署步骤。
根据你的项目信息，数据库服务器在 `106.15.36.199`。我来为你提供几种部署方案：

## 📊 当前架构分析

| 组件 | 当前配置 | 服务器 |
|------|----------|--------|
| 数据库 | MySQL @ 106.15.36.199:3306 | 远程服务器 ✅ |
| 后端 | FastAPI @ localhost:8000 | 本地开发机 |
| 前端 | Vue3 @ localhost:5173 | 本地开发机 |

---

## 🚀 部署方案推荐

### 方案一：前后端分离部署 + Nginx（推荐 ⭐）

这是最标准的生产部署方案：

```
┌─────────────────────────────────────────────┐
│              服务器 106.15.36.199            │
│  ┌──────────────┐     ┌─────────────────┐   │
│  │   Nginx      │────▶│  FastAPI后端    │   │
│  │   (80/443)   │     │  (127.0.0.1:8000)│   │
│  └──────────────┘     └─────────────────┘   │
│         │                                    │
│         ▼                                    │
│  ┌──────────────┐                            │
│  │  前端静态文件  │                            │
│  │  (dist目录)   │                            │
│  └──────────────┘                            │
└─────────────────────────────────────────────┘
```

---

## 📦 部署步骤详解

### 步骤 1：服务器环境准备

需要在服务器 `106.15.36.199` 上安装：

```bash
# 1. 安装 Python 3.9+
sudo apt update
sudo apt install python3 python3-pip python3-venv -y

# 2. 安装 Nginx
sudo apt install nginx -y

# 3. 安装 Node.js (用于构建前端)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs -y

# 4. 安装 PM2 (进程管理)
sudo npm install -g pm2
```

### 步骤 2：后端部署

```bash
# 1. 上传后端代码到服务器
scp -r backend/ root@106.15.36.199:/opt/pet-management/

# 2. SSH 登录服务器
ssh root@106.15.36.199

# 3. 创建虚拟环境
cd /opt/pet-management/backend
python3 -m venv venv
source venv/bin/activate

# 4. 安装依赖
pip install -r requirements.txt

# 5. 修改环境变量配置
cat > .env << 'EOF'
DATABASE_URL=mysql+pymysql://wxy:Wxy123..@localhost:3306/pet_management
SECRET_KEY=your-production-secret-key-min-32-characters-long
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
CORS_ORIGINS=http://106.15.36.199,http://localhost
ENVIRONMENT=production
DEBUG=False
APP_NAME=宠物管理系统
APP_VERSION=1.0.0
EOF

# 6. 使用 PM2 启动后端
pm2 start "python -m uvicorn app.main:app --host 127.0.0.1 --port 8000" \
  --name pet-backend

# 7. 设置开机自启
pm2 startup
pm2 save
```

### 步骤 3：前端构建与部署

```bash
# 1. 在本地构建前端（或在服务器上构建）
cd frontend

# 2. 修改 API 基础地址
# 创建/修改 .env.production 文件
cat > .env.production << 'EOF'
VITE_API_BASE_URL=/api
EOF

# 3. 修改 vite.config.js 移除代理（生产环境不需要）
```

创建生产环境配置 `frontend/vite.config.prod.js`：

```javascript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  base: '/',  // 基础路径
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: false
  }
})
```

```bash
# 4. 构建前端
npm run build

# 5. 上传构建结果到服务器
scp -r dist/ root@106.15.36.199:/opt/pet-management/frontend/
```

### 步骤 4：Nginx 配置

在服务器上创建 Nginx 配置文件：

```bash
sudo tee /etc/nginx/sites-available/pet-management << 'EOF'
server {
    listen 80;
    server_name 106.15.36.199;  # 或你的域名

    # 前端静态文件
    location / {
        root /opt/pet-management/frontend/dist;
        index index.html;
        try_files $uri $uri/ /index.html;  # 支持Vue Router
    }

    # 后端 API 代理
    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    # 静态资源缓存
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        root /opt/pet-management/frontend/dist;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
EOF

# 启用配置
sudo ln -sf /etc/nginx/sites-available/pet-management /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx
```

---

## 🔄 自动化部署脚本

我可以为你创建一个完整的自动化部署脚本，保存为 `deploy.sh`：

```bash
#!/bin/bash
# 部署脚本 - 在本地运行

SERVER_IP="106.15.36.199"
SERVER_USER="root"
DEPLOY_DIR="/opt/pet-management"

echo "🚀 开始部署宠物管理系统..."

# 1. 构建前端
echo "📦 构建前端..."
cd frontend
npm install
npm run build

# 2. 上传代码
echo "📤 上传代码到服务器..."
ssh ${SERVER_USER}@${SERVER_IP} "mkdir -p ${DEPLOY_DIR}"
scp -r backend ${SERVER_USER}@${SERVER_IP}:${DEPLOY_DIR}/
scp -r frontend/dist ${SERVER_USER}@${SERVER_IP}:${DEPLOY_DIR}/frontend/

# 3. 在服务器上执行部署
echo "🔧 配置服务器..."
ssh ${SERVER_USER}@${SERVER_IP} << 'REMOTE_SCRIPT'
    cd /opt/pet-management/backend
    
    # 创建虚拟环境
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    
    # 更新环境变量
    cat > .env << 'EOF'
DATABASE_URL=mysql+pymysql://wxy:Wxy123..@localhost:3306/pet_management
SECRET_KEY=your-production-secret-key-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
CORS_ORIGINS=http://106.15.36.199
ENVIRONMENT=production
DEBUG=False
APP_NAME=宠物管理系统
APP_VERSION=1.0.0
EOF
    
    # 重启后端服务
    pm2 delete pet-backend 2>/dev/null || true
    pm2 start "python -m uvicorn app.main:app --host 127.0.0.1 --port 8000" \
        --name pet-backend
    
    # 配置 Nginx
    sudo tee /etc/nginx/sites-available/pet-management << 'EOF'
server {
    listen 80;
    server_name _;
    
    location / {
        root /opt/pet-management/frontend/dist;
        index index.html;
        try_files $uri $uri/ /index.html;
    }
    
    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
EOF
    
    sudo ln -sf /etc/nginx/sites-available/pet-management /etc/nginx/sites-enabled/
    sudo systemctl restart nginx
    
    echo "✅ 部署完成!"
REMOTE_SCRIPT

echo "🎉 部署成功! 访问: http://${SERVER_IP}"
```

---

## 🔒 安全配置建议

部署后建议进行以下安全加固：

### 1. 修改后端环境变量

```bash
# .env 文件修改
SECRET_KEY=$(openssl rand -hex 32)  # 生成随机密钥
ENVIRONMENT=production
DEBUG=False
CORS_ORIGINS=http://106.15.36.199  # 只允许特定域名
```

### 2. 配置 HTTPS（推荐）

```bash
# 使用 Certbot 配置 SSL
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

### 3. 防火墙配置

```bash
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

---

## 📋 部署检查清单

| 步骤 | 操作 | 验证方式 |
|------|------|----------|
| ✅ | 后端服务运行 | `pm2 status` |
| ✅ | Nginx 配置正确 | `sudo nginx -t` |
| ✅ | 前端文件可访问 | 访问 `http://106.15.36.199` |
| ✅ | API 接口正常 | `curl http://106.15.36.199/api/health` |
| ✅ | 登录功能正常 | 使用账号 admin/admin123 登录 |

---

## ❓ 需要我帮你做什么？

1. **创建部署脚本文件** - 我可以帮你创建完整的 `deploy.sh` 脚本
2. **修改配置文件** - 更新前端和后端的配置文件以适应生产环境
3. **添加 Dockerfile** - 使用 Docker 容器化部署（更现代化）
4. **配置 CI/CD** - 使用 GitHub Actions 自动部署

你希望采用哪种方案？或者需要我帮你创建具体的部署文件？
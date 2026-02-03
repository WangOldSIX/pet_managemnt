# 阿里云服务器部署指南

## 📋 项目概述

本指南详细说明如何将宠物管理系统的前端和后端部署到阿里云服务器上。

### 当前架构

```
┌─────────────────────────────────────────────────────────┐
│                   开发环境                              │
├─────────────────────────────────────────────────────────┤
│  前端: Vue3 + Vite     │  http://localhost:5173        │
│  后端: FastAPI + Uvicorn│ http://localhost:8000        │
│  数据库: MySQL          │ 106.15.36.199:3306           │
└─────────────────────────────────────────────────────────┘

                    ↓ 部署到

┌─────────────────────────────────────────────────────────┐
│             生产环境 (阿里云服务器)                      │
│                  106.15.36.199                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────┐                                        │
│  │   Nginx     │  监听 80/443 端口                     │
│  │   (反向代理) │                                        │
│  └──────┬──────┘                                        │
│         │                                               │
│    ┌────┴─────┐                                        │
│    │          │                                        │
│  ┌──▼────┐  ┌─▼────────────────────────┐               │
│  │ 前端   │  │    后端 (FastAPI)        │               │
│  │静态文件│  │    127.0.0.1:8000        │               │
│  └───────┘  └──────┬───────────────────┘               │
│                    │                                    │
│               ┌────▼──────────────────────────────┐    │
│               │      MySQL 数据库                 │    │
│               │      localhost:3306              │    │
│               └───────────────────────────────────┘    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 技术栈

| 组件 | 技术 | 版本 |
|------|------|------|
| 后端 | Python FastAPI | 3.9+ |
| 后端服务器 | Uvicorn | 最新 |
| 前端 | Vue 3 | ^3.4.0 |
| 前端构建 | Vite | ^5.0.0 |
| Web服务器 | Nginx | 1.18+ |
| 进程管理 | PM2 | 最新 |
| 数据库 | MySQL | 8.0+ |

---

## 🔧 部署前准备工作

### 1. 本地环境检查

确保本地开发环境正常：

```bash
# 检查后端是否正常运行
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

# 在另一个终端检查前端
cd frontend
npm install
npm run dev
```

### 2. 阿里云服务器信息准备

请确认以下信息：

- 服务器IP: `106.15.36.199`
- SSH用户: `root` (或其他有sudo权限的用户)
- SSH端口: `22` (默认)
- 数据库端口: `3306`
- 数据库用户名: `wxy`
- 数据库密码: `Wxy123..`
- 数据库名: `pet_management`

### 3. 服务器安全组配置

确保阿里云安全组开放以下端口：

| 端口 | 协议 | 用途 | 来源 |
|------|------|------|------|
| 22 | TCP | SSH | 0.0.0.0/0 或 你的IP |
| 80 | TCP | HTTP | 0.0.0.0/0 |
| 443 | TCP | HTTPS | 0.0.0.0/0 |

---

## 🚀 部署步骤（推荐：Nginx + PM2）

### 步骤1: 连接服务器

```bash
# SSH连接到阿里云服务器
ssh root@106.15.36.199

# 如果提示输入密码，输入服务器密码
```

### 步骤2: 安装系统依赖

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装 Python 3.9+ 和相关工具
sudo apt install python3 python3-pip python3-venv python3-dev -y

# 安装 Node.js 18.x
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs -y

# 验证安装
python3 --version  # 应显示 Python 3.9+
node --version     # 应显示 v18.x.x
npm --version      # 应显示 9.x.x

# 安装 Nginx
sudo apt install nginx -y

# 安装 PM2 (进程管理器)
sudo npm install -g pm2

# 安装 Git (如果需要)
sudo apt install git -y
```

### 步骤3: 创建项目目录

```bash
# 创建项目根目录
sudo mkdir -p /opt/pet-management
sudo chown -R $USER:$USER /opt/pet-management

# 创建子目录
cd /opt/pet-management
mkdir -p backend frontend logs
```

### 步骤4: 部署后端

#### 方式A: 手动上传并部署（适合初次部署）

在**本地电脑**执行：

```bash
# 1. 进入后端目录
cd d:/codes/wxy/codes_of_python/Pet_mangement/backend

# 2. 打包后端代码（排除不必要的文件）
tar -czf backend.tar.gz --exclude='venv' --exclude='__pycache__' --exclude='*.pyc' --exclude='.git' .

# 3. 上传到服务器
scp backend.tar.gz root@106.15.36.199:/opt/pet-management/

# 4. 上传 requirements.txt（如果没有包含在tar包中）
scp requirements.txt root@106.15.36.199:/opt/pet-management/backend/
```

在**服务器**执行：

```bash
cd /opt/pet-management
tar -xzf backend.tar.gz
rm backend.tar.gz
cd backend

# 创建并激活虚拟环境
python3 -m venv venv
source venv/bin/activate

# 升级 pip
pip install --upgrade pip

# 安装依赖
pip install -r requirements.txt

# 创建生产环境配置文件
cat > .env << 'EOF'
# 数据库配置
DATABASE_URL=mysql+pymysql://wxy:Wxy123..@localhost:3306/pet_management

# JWT密钥配置（请修改为随机生成的密钥）
SECRET_KEY=$(openssl rand -hex 32)
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS配置（生产环境只允许特定域名）
CORS_ORIGINS=http://106.15.36.199

# 环境配置
ENVIRONMENT=production
DEBUG=False

# 应用配置
APP_NAME=宠物管理系统
APP_VERSION=1.0.0
EOF

# 测试启动后端（确保没有错误）
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000

# 按 Ctrl+C 停止测试
```

使用 PM2 管理后端进程：

```bash
# 创建 PM2 配置文件
cat > ecosystem.config.js << 'EOF'
module.exports = {
  apps: [{
    name: 'pet-backend',
    script: 'venv/bin/python',
    args: '-m uvicorn app.main:app --host 127.0.0.1 --port 8000',
    cwd: '/opt/pet-management/backend',
    autorestart: true,
    max_restarts: 10,
    min_uptime: '10s',
    max_memory_restart: '1G',
    env: {
      NODE_ENV: 'production'
    },
    error_file: '/opt/pet-management/logs/backend-error.log',
    out_file: '/opt/pet-management/logs/backend-out.log',
    log_date_format: 'YYYY-MM-DD HH:mm:ss Z'
  }]
}
EOF

# 启动后端服务
pm2 start ecosystem.config.js

# 查看服务状态
pm2 status

# 查看日志
pm2 logs pet-backend

# 设置开机自启
pm2 startup
pm2 save
```

#### 方式B: 使用 Git 克隆（如果代码已推送到 Git）

```bash
cd /opt/pet-management
git clone https://github.com/your-username/pet-management.git backend
cd backend

# 后续步骤同方式A
```

### 步骤5: 部署前端

#### 在本地构建前端

在**本地电脑**执行：

```bash
# 1. 进入前端目录
cd d:/codes/wxy/codes_of_python/Pet_mangement/frontend

# 2. 创建生产环境配置文件
cat > .env.production << 'EOF'
VITE_API_BASE_URL=/api
EOF

# 3. 修改 vite.config.js（如果需要）
# 确保配置如下：
cat > vite.config.js << 'EOF'
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
  base: '/',  // 生产环境基础路径
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: false,  // 生产环境关闭 source map
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true,  // 移除 console
        drop_debugger: true
      }
    }
  }
})
EOF

# 4. 安装依赖
npm install

# 5. 构建生产版本
npm run build

# 6. 上传构建产物到服务器
scp -r dist/* root@106.15.36.199:/opt/pet-management/frontend/
```

#### 在服务器上验证

```bash
# 检查前端文件是否上传成功
ls -la /opt/pet-management/frontend/

# 应该看到 index.html 和 assets 文件夹
```

### 步骤6: 配置 Nginx

在**服务器**上创建 Nginx 配置：

```bash
# 创建 Nginx 配置文件
sudo tee /etc/nginx/sites-available/pet-management << 'EOF'
server {
    listen 80;
    server_name 106.15.36.199;  # 如果有域名，改为域名

    # 访问日志和错误日志
    access_log /var/log/nginx/pet-management-access.log;
    error_log /var/log/nginx/pet-management-error.log;

    # 前端静态文件
    location / {
        root /opt/pet-management/frontend;
        index index.html;

        # Vue Router history 模式支持
        try_files $uri $uri/ /index.html;

        # 安全头
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-XSS-Protection "1; mode=block" always;
    }

    # 后端 API 代理
    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;

        # WebSocket 支持（如果需要）
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';

        # 传递真实 IP
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # 超时设置
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;

        # 禁用缓存
        proxy_cache_bypass $http_upgrade;
    }

    # 静态资源缓存（1年）
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        root /opt/pet-management/frontend;
        expires 1y;
        add_header Cache-Control "public, immutable";
        access_log off;
    }

    # 拒绝访问隐藏文件
    location ~ /\. {
        deny all;
        access_log off;
        log_not_found off;
    }
}
EOF

# 创建软链接启用配置
sudo ln -sf /etc/nginx/sites-available/pet-management /etc/nginx/sites-enabled/

# 删除默认配置（可选）
sudo rm -f /etc/nginx/sites-enabled/default

# 测试 Nginx 配置
sudo nginx -t

# 重启 Nginx
sudo systemctl restart nginx

# 设置 Nginx 开机自启
sudo systemctl enable nginx
```

### 步骤7: 配置防火墙

```bash
# 安装并启用 UFW 防火墙
sudo apt install ufw -y

# 允许 SSH
sudo ufw allow 22/tcp

# 允许 HTTP
sudo ufw allow 80/tcp

# 允许 HTTPS（后续配置 SSL 时）
sudo ufw allow 443/tcp

# 启用防火墙
sudo ufw enable

# 查看防火墙状态
sudo ufw status
```

---

## ✅ 部署验证

### 1. 检查后端服务

```bash
# 查看 PM2 进程状态
pm2 status

# 查看后端日志
pm2 logs pet-backend

# 测试后端 API
curl http://127.0.0.1:8000/health

# 应该返回：
# {"status":"ok","environment":"production","app_name":"宠物管理系统","version":"1.0.0"}
```

### 2. 检查 Nginx 配置

```bash
# 测试 Nginx 配置
sudo nginx -t

# 查看 Nginx 状态
sudo systemctl status nginx
```

### 3. 从外部访问

在浏览器中访问：

- 前端页面: `http://106.15.36.199`
- 后端健康检查: `http://106.15.36.199/api/health`
- API 文档: `http://106.15.36.199/api/docs`

### 4. 功能测试

- ✅ 打开登录页面
- ✅ 使用测试账号登录
- ✅ 查看仪表盘数据
- ✅ 测试其他功能模块

---

## 🔄 更新部署

### 更新后端

```bash
# 在服务器上
cd /opt/pet-management/backend

# 拉取最新代码（如果使用 Git）
git pull origin main

# 或上传新的代码文件（在本地执行）
scp -r backend/* root@106.15.36.199:/opt/pet-management/backend/

# 重启后端服务
pm2 restart pet-backend

# 查看日志确认启动成功
pm2 logs pet-backend
```

### 更新前端

```bash
# 在本地
cd frontend
npm run build

# 上传构建产物
scp -r dist/* root@106.15.36.199:/opt/pet-management/frontend/

# 在服务器上清除浏览器缓存（可选，客户端重新访问时会自动加载新文件）
# 如果需要强制刷新，可以重启 Nginx
sudo systemctl reload nginx
```

---

## 🔒 安全加固建议

### 1. 配置 HTTPS（使用 Let's Encrypt 免费证书）

```bash
# 安装 Certbot
sudo apt install certbot python3-certbot-nginx -y

# 申请 SSL 证书（需要先配置域名）
# sudo certbot --nginx -d your-domain.com

# 自动续期
sudo certbot renew --dry-run
```

### 2. 修改 SSH 端口（可选）

```bash
# 编辑 SSH 配置
sudo nano /etc/ssh/sshd_config

# 修改端口号
Port 2222  # 改为其他端口

# 禁用 root 登录（可选）
PermitRootLogin no

# 重启 SSH
sudo systemctl restart sshd
```

### 3. 配置自动备份

```bash
# 创建备份脚本
cat > /opt/backup-pet-management.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/opt/backups/pet-management"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

# 备份数据库
mysqldump -u wxy -p'Wxy123..' pet_management > $BACKUP_DIR/db_$DATE.sql

# 备份配置文件
tar -czf $BACKUP_DIR/config_$DATE.tar.gz /opt/pet-management/backend/.env

# 保留最近7天的备份
find $BACKUP_DIR -type f -mtime +7 -delete
EOF

chmod +x /opt/backup-pet-management.sh

# 添加到 crontab（每天凌晨2点备份）
(crontab -l 2>/dev/null; echo "0 2 * * * /opt/backup-pet-management.sh") | crontab -
```

### 4. 数据库安全

```bash
# 修改数据库配置
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf

# 绑定到本地（只允许本地访问）
bind-address = 127.0.0.1

# 重启 MySQL
sudo systemctl restart mysql
```

---

## 📊 监控与日志

### 1. 查看 PM2 日志

```bash
# 实时查看
pm2 logs pet-backend

# 查看错误日志
pm2 logs pet-backend --err

# 查看最近的100行
pm2 logs pet-backend --lines 100
```

### 2. 查看 Nginx 日志

```bash
# 访问日志
sudo tail -f /var/log/nginx/pet-management-access.log

# 错误日志
sudo tail -f /var/log/nginx/pet-management-error.log
```

### 3. 系统资源监控

```bash
# 安装 htop
sudo apt install htop -y

# 查看系统资源
htop

# 查看磁盘使用
df -h

# 查看内存使用
free -h
```

---

## ❓ 常见问题解决

### 问题1: 后端启动失败

**症状**: PM2 显示服务状态为 `errored`

**解决**:
```bash
# 查看详细日志
pm2 logs pet-backend --lines 50

# 常见原因：
# 1. 依赖未安装 → 重新执行 pip install -r requirements.txt
# 2. 数据库连接失败 → 检查 .env 文件中的 DATABASE_URL
# 3. 端口被占用 → 检查 8000 端口是否被其他程序占用
sudo lsof -i :8000
```

### 问题2: 前端页面空白

**症状**: 浏览器显示空白页面

**解决**:
```bash
# 检查前端文件是否正确上传
ls -la /opt/pet-management/frontend/

# 应该看到 index.html 文件

# 检查 Nginx 配置
sudo nginx -t

# 查看 Nginx 错误日志
sudo tail -f /var/log/nginx/pet-management-error.log
```

### 问题3: API 请求失败（404）

**症状**: 前端无法调用后端 API

**解决**:
```bash
# 检查后端服务是否运行
pm2 status

# 检查 API 路由
curl http://127.0.0.1:8000/health

# 检查 Nginx 代理配置
sudo cat /etc/nginx/sites-available/pet-management | grep -A 10 location /api

# 确认 proxy_pass 指向正确的地址
```

### 问题4: CORS 错误

**症状**: 浏览器控制台显示 CORS 相关错误

**解决**:
```bash
# 检查后端 .env 文件中的 CORS_ORIGINS 配置
cat /opt/pet-management/backend/.env | grep CORS

# 确保包含你的服务器 IP 或域名
CORS_ORIGINS=http://106.15.36.199

# 重启后端
pm2 restart pet-backend
```

### 问题5: 数据库连接失败

**症状**: 后端日志显示数据库连接错误

**解决**:
```bash
# 测试数据库连接
mysql -h 127.0.0.1 -u wxy -p pet_management

# 检查数据库服务状态
sudo systemctl status mysql

# 检查数据库配置
cat /opt/pet-management/backend/.env | grep DATABASE_URL
```

---

## 📝 自动化部署脚本

为了简化部署过程，可以创建自动化脚本：

### deploy.sh（在本地执行）

```bash
#!/bin/bash

set -e  # 遇到错误立即退出

# 配置变量
SERVER_IP="106.15.36.199"
SERVER_USER="root"
BACKEND_DIR="/opt/pet-management/backend"
FRONTEND_DIR="/opt/pet-management/frontend"

echo "🚀 开始部署宠物管理系统..."

# 1. 构建前端
echo "📦 [1/4] 构建前端..."
cd frontend
npm install
npm run build
cd ..

# 2. 打包后端
echo "📦 [2/4] 准备后端代码..."
cd backend
tar -czf backend.tar.gz --exclude='venv' --exclude='__pycache__' --exclude='*.pyc' --exclude='.git' .
cd ..

# 3. 上传到服务器
echo "📤 [3/4] 上传代码到服务器..."
scp backend.tar.gz ${SERVER_USER}@${SERVER_IP}:${BACKEND_DIR}/
scp -r frontend/dist/* ${SERVER_USER}@${SERVER_IP}:${FRONTEND_DIR}/

# 4. 在服务器上部署
echo "🔧 [4/4] 在服务器上配置..."
ssh ${SERVER_USER}@${SERVER_IP} << 'ENDSSH'
cd /opt/pet-management/backend

# 解压后端代码
tar -xzf backend.tar.gz
rm backend.tar.gz

# 重启后端服务
pm2 restart pet-backend

# 重新加载 Nginx
sudo systemctl reload nginx

echo "✅ 部署完成!"
ENDSSH

echo "🎉 部署成功! 访问: http://${SERVER_IP}"
```

使用方法：
```bash
# 给脚本执行权限
chmod +x deploy.sh

# 执行部署
./deploy.sh
```

---

## 📚 附录

### A. 目录结构

服务器上的目录结构：

```
/opt/pet-management/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── crud/
│   │   ├── db/
│   │   ├── schemas/
│   │   └── service/
│   ├── venv/                    # Python 虚拟环境
│   ├── .env                     # 环境变量配置
│   ├── ecosystem.config.js      # PM2 配置
│   └── requirements.txt         # Python 依赖
│
├── frontend/
│   ├── index.html
│   ├── assets/                  # 静态资源
│   └── (其他前端文件)
│
└── logs/                        # 日志文件
    ├── backend-error.log
    ├── backend-out.log
    └── (其他日志)
```

### B. 端口映射

| 服务 | 内部地址 | 外部访问 | 说明 |
|------|----------|----------|------|
| Nginx | 80/443 | http://106.15.36.199 | Web 服务入口 |
| FastAPI | 127.0.0.1:8000 | 通过 Nginx 代理 | 后端 API 服务 |
| MySQL | 127.0.0.1:3306 | 不对外开放 | 数据库服务 |

### C. 有用的命令

```bash
# PM2 命令
pm2 list                          # 查看所有进程
pm2 start <name>                 # 启动进程
pm2 stop <name>                  # 停止进程
pm2 restart <name>               # 重启进程
pm2 delete <name>                # 删除进程
pm2 monit                        # 实时监控
pm2 logs <name>                  # 查看日志

# Nginx 命令
sudo nginx -t                    # 测试配置
sudo systemctl reload nginx      # 重载配置
sudo systemctl restart nginx     # 重启服务
sudo systemctl status nginx      # 查看状态

# 系统命令
df -h                            # 磁盘使用情况
free -h                          # 内存使用情况
top / htop                       # 进程监控
netstat -tlnp                    # 查看端口占用
```

---

## 🎯 部署检查清单

部署完成后，请逐项检查：

- [ ] 服务器防火墙已开放 80、443 端口
- [ ] Python 3.9+ 已安装
- [ ] Node.js 18.x 已安装
- [ ] Nginx 已安装并运行
- [ ] 后端依赖已安装（requirements.txt）
- [ ] 后端 .env 文件配置正确
- [ ] PM2 后端服务运行正常
- [ ] 前端构建产物已上传
- [ ] Nginx 配置正确并生效
- [ ] 数据库连接正常
- [ ] 前端页面可正常访问
- [ ] API 接口调用正常
- [ ] 用户登录功能正常
- [ ] 日志输出正常
- [ ] 配置了自动备份（可选）

---

## 📞 技术支持

如果在部署过程中遇到问题：

1. 查看日志文件定位错误
2. 参考本文档的"常见问题解决"部分
3. 检查服务器资源使用情况

祝你部署顺利！🎉

# 宠物管理系统前端

基于 Vue 3 + Vite + Element Plus 的宠物管理系统前端应用

## 技术栈

- Vue 3 - 渐进式 JavaScript 框架
- Vite - 下一代前端构建工具
- Element Plus - Vue 3 组件库
- Pinia - Vue 状态管理
- Vue Router - Vue 路由
- Axios - HTTP 客户端

## 功能模块

- 用户认证（登录/登出）
- 仪表盘（数据统计）
- 宠物管理
- 用户管理
- 服务管理
- 订单管理
- 寄养管理
- 健康记录

## 开发指南

### 安装依赖

```bash
npm install
```

### 启动开发服务器

```bash
npm run dev
```

访问 http://localhost:5173

### 构建生产版本

```bash
npm run build
```

### 预览生产构建

```bash
npm run preview
```

## 项目结构

```
frontend/
├── public/           # 静态资源
├── src/
│   ├── api/         # API 接口
│   ├── assets/      # 资源文件
│   ├── components/  # 公共组件
│   ├── layout/      # 布局组件
│   ├── router/      # 路由配置
│   ├── stores/      # 状态管理
│   ├── utils/       # 工具函数
│   ├── views/       # 页面组件
│   ├── App.vue      # 根组件
│   └── main.js      # 入口文件
├── index.html       # HTML 模板
├── package.json     # 项目配置
└── vite.config.js   # Vite 配置
```

## API 配置

后端 API 地址配置在 `vite.config.js` 中：

```javascript
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true
    }
  }
}
```

## 环境要求

- Node.js >= 16.0.0
- npm >= 8.0.0

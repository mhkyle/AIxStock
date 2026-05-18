# 🚀 AIxStock Frontend

> 📈 基于 React + TypeScript + Vite 的智能股票分析预测前端应用

---

## ✨ 技术栈

| 🔰 类别 | 📦 依赖 |
|----------|----------|
| ⚛️ 框架 | React 19 · TypeScript 5.9 |
| ⚡ 构建 | Vite 8 · @vitejs/plugin-react |
| 🎨 样式 | Tailwind CSS 4 · tw-animate-css |
| 🧩 UI 组件 | shadcn/ui (Radix UI) · lucide-react |
| 🔧 工具库 | clsx · class-variance-authority · tailwind-merge |
| 🔤 字体 | @fontsource-variable/inter |
| ✅ 代码质量 | ESLint 9 · Prettier · typescript-eslint |

## 🔧 环境要求

- 🟢 Node.js >= 18
- 📦 npm >= 9

## 🏃 快速开始

```bash
# 📂 进入前端目录
cd frontend/aix-stock-fe

# 📥 安装依赖
npm install

# 🔥 启动开发服务器（默认 http://localhost:5173）
npm run dev

# 📦 构建生产版本
npm run build

# 👀 预览构建结果
npm run preview
```

## 📋 可用脚本

| 📝 命令 | 💡 说明 |
|----------|----------|
| `npm run dev` | 🔥 启动 Vite 开发服务器，支持 HMR 热更新 |
| `npm run build` | 🏗️ TypeScript 类型检查 + Vite 生产构建，输出到 `dist/` |
| `npm run preview` | 👁️ 本地预览 `dist/` 构建产物 |
| `npm run lint` | 🔍 ESLint 代码检查 |
| `npm run format` | ✨ Prettier 格式化 `ts/tsx` 文件 |
| `npm run typecheck` | 🧪 仅运行 TypeScript 类型检查，不输出文件 |

## 📁 项目结构

```
aix-stock-fe/
├── 📦 public/
│   └── 🎯 stock-icon.svg       # 网站图标
├── 📂 src/
│   ├── 🖼️ assets/              # 静态资源
│   ├── 🧩 components/           # 公共组件
│   │   └── 🌗 theme-provider.tsx
│   ├── 🛠️ lib/                  # 工具函数
│   ├── 📄 App.tsx               # 根组件
│   ├── 🚪 main.tsx              # 入口文件
│   └── 🎨 index.css             # 全局样式
├── 📄 index.html                # HTML 模板
├── ⚙️ vite.config.ts            # Vite 配置（含 @ 路径别名）
├── 🔷 tsconfig.json             # TypeScript 配置
├── 📦 package.json
└── 📖 README.md
```

## 🔗 路径别名

通过 `vite.config.ts` 和 `tsconfig.json` 配置了 `@` 路径别名，指向 `src/`：

```ts
import { Button } from "@/components/ui/button"
```

## 🗺️ 路线图

- [ ] 📊 **ECharts** — K 线图（蜡烛图）、走势曲线图、成交量柱状图等股票行情可视化
- [ ] 🌐 行情数据 API 对接
- [ ] 🤖 AI 买卖预测模型接入

---

## ⚠️ License

**All Rights Reserved.** 本项目代码仅供作者（Alan Wu）和团队使用。

- ❌ 禁止任何人以任何形式复制、分发、修改或使用本项目的任何部分
- ❌ 禁止用于商业用途
- ❌ 禁止用于个人学习以外的任何目的
- ❌ 未经作者明确书面许可，不得将本代码用于任何其他项目

> 💡 **不要抄袭，不要外传。**

---

<p align="center">👨‍💻 Maintained with ❤️ by <strong>Alan Wu</strong></p>

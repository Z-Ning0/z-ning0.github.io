# 阿柠下班了吗

个人站源码。线上地址：**https://ningcraft.com/**

一个纯静态、自包含的门面页——没有框架、没有构建工具、没有外部 CDN 依赖，两个 HTML 文件就是全部。

## 结构

```
site/
├── index.html          # 门面（状态行 / 配色开关 / 终端彩蛋）
└── 404.html            # 这个页面下班了
.github/workflows/
└── pages.yml           # push 到 master → 部署 site/ 到 GitHub Pages
CNAME                   # ningcraft.com（自定义域名，别删）
```

## 本地预览

```bash
cd site
python -m http.server 8000
# 打开 http://127.0.0.1:8000/
```

## 部署

推送到 `master` 即自动部署，无需手动操作：

```bash
git add -A && git commit -m "feat(site): ..." && git push
```

Actions 跑完（约 1 分钟）后线上生效。仓库 Settings → Pages 的 Source 是 **GitHub Actions**，自定义域名 `ningcraft.com`。

## 历史说明

本仓库早期是 [Huxpro/huxpro.github.io](https://github.com/Huxpro/huxpro.github.io) 的 fork（Jekyll 主题）。2026-10-11 起切换为纯静态站；旧主题文件已于 2026-10-18 从 `master` 移除——需要找回旧主题，可查看该日期之前的提交历史。

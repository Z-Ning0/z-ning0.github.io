# 阿柠下班了吗

[个人站](https://ningcraft.com/) · [现在](https://ningcraft.com/now.html) · [RSS](https://ningcraft.com/rss.xml)

- `site/`：发布的静态页面与资源，含条目流、长文和学习短记。
- `notes/`：学习短记的 Markdown 正本。
- `.github/workflows/pages.yml`：推送到 `main` 后，将 `site/` 部署到 GitHub Pages。

## 本地预览

```bash
python -m http.server 8000 --bind 127.0.0.1 --directory site
```

打开 <http://127.0.0.1:8000/>。

## 历史

早期站点使用 [Huxpro 的 Jekyll 主题](https://github.com/Huxpro/huxpro.github.io)，感谢原作者与贡献者。旧 `master` 保留完整历史；当前静态站在 `main` 维护。

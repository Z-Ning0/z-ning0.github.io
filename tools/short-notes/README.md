# 学习短记生成工具

从 Markdown 生成短记 HTML 和分享图。它只写本地候发布目录，不连接 GitHub、不更新 RSS 或列表，也不自动发布。

## 准备

- Windows、Python 3.10+、微软雅黑和 Consolas（脚本从 `C:/Windows/Fonts` 读取）。依赖：`python -m pip install markdown-it-py Pillow`。
- 用已部署的 `site/` 创建一个隔离副本；其中需有 `assets/site.css` 和带 48 px 图层的 `favicon.ico`。
- `--generator` 指向站点本地生成器所在目录（需要 `build_site.py` 和 `site_brand.py`）。该生成器不由本工具安装，也不在 Pages 运行。
- Markdown 第一行是 `# 标题`。slug 只用小写字母、数字和连字符。

## 普通短记

命令中的参数值为示例，请替换为实际稿件及本地路径：

```bash
python tools/short-notes/build_note.py article.md --slug article --output site-copy --generator generator-copy
```

会生成 `notes/article/index.html` 和 `notes/article/share.png`。同名笔记默认拒绝覆盖。首页、列表和 RSS 不变。

## 可选：实验桌

给上面的命令追加 `--experiment --example-label 目录树 --feature-output next-feature.json`。正文中需要一个示例用的 `text` 代码块，以及一个 `<details><summary>问题</summary>…</details>`，其内部第一个 `text` 代码块是实际输出。生成的实验卡只用问题和示例，不放答案。

只有确定要选为首页实验时，才把 `next-feature.json` 复制为**生成器副本**里的 `experiment.json`，再生成该候发布目录的首页：

```bash
python generator-copy/build_site.py --index-only --output-dir site-copy
```

先用本地 HTTP 预览正文、折叠答案及图片；如启用精选，再核实首页入口指向该短记。确认要上线时，单独发布验收过的页面和图片，不要提交整个候发布目录。Pages 只部署 `site/`，不会在部署期间运行此工具。

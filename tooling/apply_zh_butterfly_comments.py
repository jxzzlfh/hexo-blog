# -*- coding: utf-8 -*-
"""为站点根目录 _config.butterfly.yml 批量添加中文说明（在英文原注释前加【中文】前缀）。

用法：从主题复制最新配置后执行
  python tooling/apply_zh_butterfly_comments.py

注意：不要放在 scripts/ 目录下，Hexo 会把该目录下所有文件当作 JS 插件加载。
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PATH = ROOT / "_config.butterfly.yml"

# 整行精确替换：键为主题文件中的完整一行（不含换行）
LINE_MAP = {
    "# Hexo Butterfly Theme Configuration": "# 【主题配置】Hexo Butterfly Theme Configuration",
    "# If you have any questions, please refer to the documentation": "# 【说明】有问题请查阅官方文档（下方链接）",
    "# Chinese: https://butterfly.js.org/": "# 【中文文档】https://butterfly.js.org/",
    "# English: https://butterfly.js.org/en/": "# 【英文文档】https://butterfly.js.org/en/",
    "# Navigation Settings": "# 【导航栏】Navigation Settings",
    "# Code Blocks Settings": "# 【代码块】Code Blocks Settings",
    "# Image Settings": "# 【图片 / 封面 / 背景】Image Settings",
    "# Index page settings": "# 【首页布局】Index page settings",
    "# Post Settings": "# 【文章页】Post Settings",
    "# Footer Settings": "# 【页脚】Footer Settings",
    "# Aside Settings": "# 【侧边栏】Aside Settings",
    "# Bottom right button": "# 【右下角悬浮按钮】Bottom right button",
    "# Global Settings": "# 【全局：锚点/复制/字数/不蒜子等】Global Settings",
    "# Math": "# 【数学公式 MathJax / KaTeX】Math",
    "# Search": "# 【搜索】Search",
    "# Share System": "# 【分享】Share System",
    "# Comments System": "# 【评论系统】Comments System",
    "# Chat Services": "# 【在线客服 / 聊天插件】Chat Services",
    "# Analysis": "# 【访问统计 / 分析】Analysis",
    "# Advertisement": "# 【广告】Advertisement",
    "# Verification": "# 【站长验证 meta】Verification",
    "# Beautify / Effect": "# 【美化与动效】Beautify / Effect",
    "# Lightbox Settings": "# 【图片灯箱】Lightbox Settings",
    "# Tag Plugins settings": "# 【标签插件：Series/Mermaid 等】Tag Plugins settings",
    "# Other Settings": "# 【其它：PJAX/懒加载/PWA/注入/CDN】Other Settings",
    "# Social media links": "# 【社交媒体链接】Social media links",
    "# Formal:": "# 【格式说明】Formal:",
    "# Sponsor/reward": "# 【打赏】Sponsor/reward",
    "# Post edit": "# 【在线编辑文章链接】Post edit",
    "# Related Articles": "# 【相关文章】Related Articles",
    "# Read Mode": "# 【阅读模式】Read Mode",
    "# Dark Mode": "# 【深色模式】Dark Mode",
    "# Background effects": "# 【背景动效】Background effects",
    "# Series": "# 【系列文章】Series",
    "# Note - Bootstrap Callout": "# 【Note 提示框样式】Note - Bootstrap Callout",
    "# Open graph meta tags": "# 【Open Graph 分享卡片】Open graph meta tags",
    "# Structured Data": "# 【结构化数据 SEO】Structured Data",
    "# Inject": "# 【自定义注入 head/body】Inject",
    "# CDN Settings": "# 【CDN 加速】CDN Settings",
    "# Google Adsense": "# 【谷歌广告】Google Adsense",
    "# Insert ads manually": "# 【手动广告位】Insert ads manually",
    "# Theme color for customize": "# 【主题色自定义】Theme color for customize",
    "# Loading Animation": "# 【加载动画】Loading Animation",
    "# Page Transition": "# 【页面过渡动画】Page Transition",
    "# Typewriter Effect": "# 【打字机爆炸特效】Typewriter Effect",
    "# Lazyload": "# 【图片懒加载】Lazyload",
    "# PWA": "# 【渐进式应用 PWA】PWA",
    "# Snackbar - Toast Notification": "# 【右下角 Snackbar 提示】Snackbar - Toast Notification",
    "# Instant.page": "# 【Instant.page 预加载】Instant.page",
    "# Algolia Search": "# 【Algolia 搜索】Algolia Search",
    "# Local Search": "# 【本地搜索】Local Search",
    "# Docsearch": "# 【Docsearch】Docsearch",
    "# Share.js": "# 【Share.js】Share.js",
    "# AddToAny": "# 【AddToAny】AddToAny",
    "# Disqus": "# 【Disqus】Disqus",
    "# Alternative Disqus - Render comments with Disqus API": "# 【DisqusJS】Alternative Disqus - Render comments with Disqus API",
    "# Livere": "# 【来必力 Livere】Livere",
    "# Gitalk": "# 【Gitalk】Gitalk",
    "# Valine": "# 【Valine】Valine",
    "# Utterances": "# 【Utterances】Utterances",
    "# Facebook Comments Plugin": "# 【Facebook 评论】Facebook Comments Plugin",
    "# Twikoo": "# 【Twikoo】Twikoo",
    "# Giscus": "# 【Giscus】Giscus",
    "# Remark42": "# 【Remark42】Remark42",
    "# Artalk": "# 【Artalk】Artalk",
    "# canvas_ribbon": "# 【Canvas 彩带】canvas_ribbon",
    "# Fluttering Ribbon": "# 【飘动彩带】Fluttering Ribbon",
    "# canvas_nest": "# 【Canvas Nest 线条背景】canvas_nest",
    "# Mouse click effects: fireworks": "# 【鼠标点击烟花】Mouse click effects: fireworks",
    "# Mouse click effects: Heart symbol": "# 【鼠标点击爱心】Mouse click effects: Heart symbol",
    "# Mouse click effects: words": "# 【鼠标点击文字】Mouse click effects: words",
    "# Mermaid": "# 【Mermaid 图表】Mermaid",
    "# chartjs": "# 【Chart.js】chartjs",
    "# ABCJS - The ABC Music Notation Plugin": "# 【ABC 乐谱】ABCJS - The ABC Music Notation Plugin",
    "# Replace Broken Images": "# 【图片加载失败占位图】Replace Broken Images",
    "# A simple 404 page": "# 【404 页面】A simple 404 page",
    "# Article layout on the homepage": "# 【首页文章卡片布局】Article layout on the homepage",
    "# Display the article introduction on homepage": "# 【首页文章摘要】Display the article introduction on homepage",
    "# The subtitle on homepage": "# 【首页副标题 / 打字机】The subtitle on homepage",
    "# Displays outdated notice for a post": "# 【文章过期提示】Displays outdated notice for a post",
    "# Conversion between Traditional and Simplified Chinese": "# 【简繁转换】Conversion between Traditional and Simplified Chinese",
    "# Busuanzi count for PV / UV in site": "# 【不蒜子 PV/UV】Busuanzi count for PV / UV in site",
    "# About the per_page": "# 【数学公式：是否每页加载】About the per_page",
    "# Need to install the hexo-wordcount plugin": "# 【需装 hexo-wordcount 插件】Need to install the hexo-wordcount plugin",
    "# Don't modify the following settings unless you know how they work": "# 【勿随意修改】Don't modify the following settings unless you know how they work",
    "# Global font settings": "# 【全站字体】Global font settings",
    "# Font settings for the site title and site subtitle": "# 【标题字体】Font settings for the site title and site subtitle",
    "# The setting of divider icon": "# 【分隔线图标】The setting of divider icon",
    "# Configuration for beautifying the content of the article": "# 【标题美化为图标前缀】Configuration for beautifying the content of the article",
    "# Add the vendor prefixes to ensure compatibility": "# 【CSS 厂商前缀】Add the vendor prefixes to ensure compatibility",
}

INDENT_MAP = {
    "  # Navigation bar logo image": "  # 【导航栏 Logo】Navigation bar logo image",
    "  # Whether to fix navigation bar": "  # 【是否固定顶栏】Whether to fix navigation bar",
    "  # Code block theme: darker / pale night / light / ocean / false": "  # 【代码块配色】Code block theme: darker / pale night / light / ocean / false",
    "  # Code block height limit (unit: px)": "  # 【代码块最大高度】Code block height limit (unit: px)",
    "  # Toolbar": "  # 【工具栏：复制/语言等】Toolbar",
    "  # Disable the cover or not": "  # 【是否启用封面】Disable the cover or not",
    "  # When cover is not set, the default cover is displayed": "  # 【默认封面】When cover is not set, the default cover is displayed",
    "  # Home Page": "  # 【首页列表元信息】Home Page",
    "  # Typewriter Effect": "  # 【打字机特效】Typewriter Effect",
    "  # Customize typed.js": "  # 【typed.js 参数】Customize typed.js",
    "  # If you set method to 2 or 3, the length need to config": "  # 【摘要长度】If you set method to 2 or 3, the length need to config",
    "  # Only for post": "  # 【仅文章页】Only for post",
    "  # Number of posts displayed": "  # 【显示篇数】Number of posts displayed",
    "  # Show the button to hide the aside in bottom right button": "  # 【隐藏侧栏按钮】Show the button to hide the aside in bottom right button",
    "  # Position: left / right": "  # 【侧栏位置】Position: left / right",
    "  # Toggle Button to switch dark/light mode": "  # 【深浅色切换按钮】Toggle Button to switch dark/light mode",
    "  # Chat Button [recommend]": "  # 【右下角聊天按钮】Chat Button [recommend]",
    "  # For self-hosted setups, configure the hostname of the Umami instance": "  # 【自建 Umami 地址】For self-hosted setups, configure the hostname of the Umami instance",
    "  # Insert ads in the index (every three posts)": "  # 【首页信息流广告】Insert ads in the index (every three posts)",
    "  # Insert ads in aside": "  # 【侧栏广告】Insert ads in aside",
    "  # Insert ads in the post (before pagination)": "  # 【文章内广告】Insert ads in the post (before pagination)",
    "  # The CDN provider for internal and third-party scripts": "  # 【CDN 提供商】The CDN provider for internal and third-party scripts",
    "  # Add version number to url, true or false": "  # 【URL 是否带版本号】Add version number to url, true or false",
}


def main():
    text = PATH.read_text(encoding="utf-8")
    for old, new in sorted(LINE_MAP.items(), key=lambda x: -len(x[0])):
        text = text.replace(old + "\n", new + "\n")
        text = text.replace(old + "\r\n", new + "\r\n")
    for old, new in sorted(INDENT_MAP.items(), key=lambda x: -len(x[0])):
        text = text.replace(old + "\n", new + "\n")
        text = text.replace(old + "\r\n", new + "\r\n")
    PATH.write_text(text, encoding="utf-8")
    print("OK:", PATH)


if __name__ == "__main__":
    main()

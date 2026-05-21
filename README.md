
# 电商商品价格自动化采集与对比工具

## ⚠️ 重要提示

**本工具需要配置抖音 Cookie 才能获取真实数据！**

请先阅读 [Cookie 配置指南](./COOKIE_SETUP_GUIDE.md) 完成配置。

## 项目简介

本工具能够从抖音电商平台批量抓取商品信息，自动清洗去重数据，按价格排序，并提供可视化图表和性价比推荐。

## 功能特点

- ✅ **真实数据采集**：使用抖音 Cookie 获取真实的商品数据
- ✅ 支持按关键词搜索采集商品
- ✅ 抓取商品名称、价格、销量、店铺评分、网址链接
- ✅ 自动数据清洗与去重
- ✅ 按价格从低到高排序
- ✅ 商品横向对比表格
- ✅ 价格分布直方图
- ✅ 价格-销量关系图表
- ✅ 性价比推荐标注（Top 3）

## 快速开始

### 1. 配置抖音 Cookie（必需）

```bash
python -m config.setup_cookie
```

按照提示获取并配置 Cookie。详细步骤请查看 [Cookie 配置指南](./COOKIE_SETUP_GUIDE.md)

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 运行程序

**命令行模式：**
```bash
python cli.py -k "耳机"
```

**Web 模式：**
```bash
python app.py
```
访问 http://localhost:5000

## 配置说明

### 获取 Cookie

1. 打开浏览器访问 https://www.douyin.com/
2. 登录账号
3. 按 F12 打开开发者工具 → Network 选项卡
4. 在页面上任意操作，筛选 cookie 请求
5. 复制完整的 Cookie 字符串

详细教程：[Cookie 配置指南](./COOKIE_SETUP_GUIDE.md)

### 常见问题

- **Cookie 过期**：重新获取并更新配置
- **数据为空**：检查 Cookie 是否包含 `odin_tt` 字段
- **请求失败**：减少采集页数，避免触发反爬虫

## 项目结构

```
douyin_crawler/
├── app.py                    # Web服务入口
├── cli.py                    # 命令行工具入口
├── config/
│   ├── settings.py           # 全局配置
│   ├── douyin_config.py      # 抖音认证配置
│   └── setup_cookie.py       # Cookie配置向导
├── crawler/
│   ├── api_client.py         # HTTP请求封装
│   └── douyin_crawler.py     # 抖音爬虫核心
├── models/
│   └── product.py            # 商品数据模型
├── processor/
│   └── data_processor.py     # 数据处理服务
├── visualizer/
│   └── chart_generator.py    # 图表生成器
├── templates/
│   └── index.html            # Web页面模板
├── utils/
│   └── helpers.py            # 辅助函数
└── requirements.txt          # 依赖列表
```

## 使用示例

### 命令行使用

```bash
# 基本搜索
python cli.py -k "耳机"

# 采集多页数据
python cli.py -k "手机" -p 3

# 保存数据
python cli.py -k "电脑" -s

# 生成可视化图表
python cli.py -k "耳机" -v
```

### Web 界面使用

1. 启动服务：`python app.py`
2. 打开浏览器访问 http://localhost:5000
3. 输入关键词并搜索

## 性价比计算公式

```
性价比得分 = (店铺评分 / 5) × (log(销量+1) / log(最大销量+1)) / (价格 / 1000)
```

## 注意事项

1. ⚠️ 请先配置有效的抖音 Cookie
2. 请合理控制采集频率，避免给目标网站带来压力
3. 本工具仅用于学习和研究目的
4. 使用前请确保遵守目标平台的使用条款
5. Cookie 会过期，如无法获取数据请更新 Cookie

# 下载说明

## 版本信息
- **版本号**: v1.0.0
- **发布日期**: 2026-05-21
- **文件大小**: 45KB

## 下载方式

### 方式一：直接下载源码包
```bash
# 克隆指定版本
git clone --branch v1.0.0 https://github.com/aa7961766/solo.git

# 或下载压缩包
wget https://github.com/aa7961766/solo/archive/refs/tags/v1.0.0.tar.gz
```

### 方式二：从 GitHub 页面下载
访问以下链接下载源码：
- **ZIP 格式**: https://github.com/aa7961766/solo/archive/refs/heads/main.zip
- **Tar.gz 格式**: https://github.com/aa7961766/solo/archive/refs/heads/main.tar.gz

### 方式三：通过 Release 页面
访问：https://github.com/aa7961766/solo/releases/tag/v1.0.0

## 安装步骤

1. **解压文件**
```bash
tar -xzf v1.0.0.tar.gz
cd solo-1.0.0
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **运行程序**

命令行模式：
```bash
python cli.py -k "耳机"
```

Web 服务模式：
```bash
python app.py
```

## 功能特点

✅ 支持抖音电商平台商品搜索采集  
✅ 自动数据清洗与去重  
✅ 按价格排序和性价比分析  
✅ 可视化图表生成  
✅ 命令行和Web界面双模式  
✅ 运行时自动安装依赖  

## 项目结构

```
douyin_crawler/
├── app.py                    # Web服务入口
├── cli.py                    # 命令行工具入口
├── config/
│   └── settings.py           # 全局配置
├── crawler/
│   ├── api_client.py         # HTTP请求封装
│   └── douyin_crawler.py     # 抖音爬虫核心
├── data/                     # 数据目录
├── models/
│   └── product.py            # 商品数据模型
├── processor/
│   └── data_processor.py     # 数据处理服务
├── templates/
│   └── index.html            # Web页面模板
├── utils/
│   └── helpers.py            # 辅助函数
├── visualizer/
│   └── chart_generator.py    # 图表生成器
└── requirements.txt          # 依赖列表
```

## 使用示例

### 命令行使用
```bash
# 基本搜索
python cli.py -k "手机"

# 采集多页数据
python cli.py -k "电脑" -p 3

# 保存数据
python cli.py -k "耳机" -s

# 生成可视化图表
python cli.py -k "耳机" -v

# 完整功能
python cli.py -k "手机" -p 3 -s -v
```

### Web 界面使用
```bash
python app.py
```
访问 http://localhost:5000

## 注意事项

1. 请合理控制采集频率，避免给目标网站带来压力
2. 本工具仅用于学习和研究目的
3. 使用前请确保遵守目标平台的使用条款
4. 部分平台可能需要登录认证才能获取数据

## 更新日志

### v1.0.0 (2026-05-21)
- 初始版本发布
- 支持抖音电商平台商品搜索
- 提供数据清洗、去重、排序功能
- 支持性价比分析和可视化图表
- 双模式运行（命令行 + Web界面）
- 运行时自动安装依赖

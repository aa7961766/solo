# 抖音 Cookie 配置指南

## ⚠️ 重要说明

抖音商品搜索 API 需要有效的 Cookie 才能获取真实数据。本工具不会使用假数据或演示数据。

## 配置步骤

### 第一步：获取抖音 Cookie

1. **打开浏览器**
   - 使用 Chrome、Edge 或 Firefox 浏览器
   - 建议使用无痕/隐私模式

2. **访问抖音**
   - 访问 https://www.douyin.com/
   - 登录您的账号（已登录可跳过）

3. **打开开发者工具**
   - 按 `F12` 打开开发者工具
   - 或右键点击页面 → 选择"检查"

4. **切换到 Network（网络）选项卡**
   - 点击 "Network" 或 "网络" 标签
   - 勾选 "Preserve log"（保留日志）

5. **筛选 Cookie 请求**
   - 在 Filter（筛选器）输入框中输入：`cookie`
   - 或者输入：`odin_tt`

6. **触发请求**
   - 在页面上点击任意视频
   - 或滚动页面加载内容
   - 或刷新页面

7. **获取 Cookie**
   - 点击任意一个网络请求
   - 在右侧找到 "Headers" 或 "请求标头"
   - 向下滚动找到 "cookie:" 字段
   - **复制整个 Cookie 字符串**

### 第二步：配置 Cookie

运行配置向导：

```bash
python -m config.setup_cookie
```

按照提示粘贴 Cookie 并保存。

### 第三步：测试配置

运行程序测试是否成功：

```bash
python cli.py -k "耳机"
```

## 常见问题

### Q1: 为什么需要 Cookie？

抖音 API 要求请求必须携带有效的 Cookie 才能返回数据。这是抖音的防爬虫机制。

### Q2: Cookie 会过期吗？

是的，Cookie 会过期。如果突然无法获取数据，请尝试更新 Cookie。

### Q3: 我的 Cookie 安全吗？

您的 Cookie 只保存在本地配置文件 `config/douyin_config.json` 中，不会上传到任何服务器。

### Q4: 获取到的数据不完整怎么办？

1. 尝试更新 Cookie（使用最新登录的账号）
2. 减少请求频率（减少页数）
3. 检查是否触发了反爬虫机制

### Q5: 出现 "invalid_app" 错误怎么办？

这表示 Cookie 无效或已过期。请：
1. 重新登录抖音账号
2. 获取新的 Cookie
3. 更新配置文件

## Cookie 格式示例

有效的抖音 Cookie 应该包含以下关键字段：

```
odin_tt=xxx; 
sessionid_ss=xxx; 
sid_tt=xxx; 
sid_guard=xxx; 
```

**特别注意**：`odin_tt` 字段是必需的！

## 技术细节

抖音 API 请求需要以下关键参数：

- **Headers**：
  - `User-Agent`: 浏览器标识
  - `Cookie`: 认证信息
  - `Referer`: 来源页面

- **Query Parameters**：
  - `keyword`: 搜索关键词
  - `count`: 每页数量
  - `cursor`: 分页游标
  - `device_id`: 设备标识（可选）

## 免责声明

- 本工具仅供学习和研究使用
- 请遵守抖音平台的使用条款
- 不要过度频繁地请求数据
- 合理使用，避免对服务器造成压力

## 获取帮助

如果配置过程中遇到问题：
1. 检查 Cookie 是否包含 `odin_tt` 字段
2. 确保 Cookie 是完整的（不是截断的）
3. 尝试重新获取 Cookie

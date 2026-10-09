# Web Scraper Pro - MCP Server

让AI能抓取任何网站的内容、链接、元数据和邮箱。

## 功能

1. **scrape_website** - 抓取网站完整内容
2. **extract_links** - 提取网站所有链接
3. **extract_metadata** - 提取元数据（标题、描述、图片）
4. **scrape_multiple_pages** - 批量抓取多个页面
5. **find_emails_on_page** - 在网站上找邮箱

## 如何发布到Mize

### 第一步：注册Mize账号
1. 打开 https://mcpize.com/
2. 点击 Sign Up
3. 用GitHub账号登录（推荐）

### 第二步：连接GitHub
1. 在Mize后台，点击 "Add New Server"
2. 连接你的GitHub账号
3. 选择这个仓库

### 第三步：设置价格
- 免费额度：每月25,000次请求
- 付费订阅：建议$9/月或$19/月
- 你拿80%收入

### 第四步：发布
1. 点击 "Deploy"
2. 30秒自动部署
3. 上线！

## 定价建议

| 方案 | 价格 | 包含 |
|------|------|------|
| Free | $0 | 100次/月 |
| Pro | $9/月 | 10,000次/月 |
| Business | $29/月 | 100,000次/月 |

## 技术栈

- Python 3.10+
- FastMCP
- httpx
- BeautifulSoup4

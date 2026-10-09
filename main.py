"""
Web Scraper MCP Server
让AI能抓取任何网站的内容、链接和结构化数据
"""
from fastmcp import FastMCP
import httpx
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse

mcp = FastMCP("Web Scraper Pro")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

@mcp.tool()
def scrape_website(url: str) -> str:
    """
    抓取网站完整内容，返回干净的文本
    
    Args:
        url: 要抓取的网站URL
        
    Returns:
        网站的干净文本内容（最多10000字符）
    """
    try:
        with httpx.Client(follow_redirects=True, timeout=30, headers=HEADERS) as client:
            response = client.get(url)
            response.raise_for_status()
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 移除不需要的元素
        for element in soup(["script", "style", "nav", "footer", "header", "aside", "advertisement"]):
            element.decompose()
        
        # 提取标题
        title = soup.title.string.strip() if soup.title else "No title"
        
        # 提取正文
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        clean_lines = [line for line in lines if line and len(line) > 1]
        clean_text = '\n'.join(clean_lines)
        
        result = f"标题: {title}\n\n内容:\n{clean_text[:8000]}"
        return result
        
    except Exception as e:
        return f"抓取失败: {str(e)}"


@mcp.tool()
def extract_links(url: str) -> list:
    """
    提取网站所有链接，带锚文本
    
    Args:
        url: 要提取链接的网站URL
        
    Returns:
        链接列表，每个包含text和href
    """
    try:
        with httpx.Client(follow_redirects=True, timeout=30, headers=HEADERS) as client:
            response = client.get(url)
            response.raise_for_status()
            
        soup = BeautifulSoup(response.text, 'html.parser')
        base_url = str(response.url)
        
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            # 转成绝对URL
            absolute_url = urljoin(base_url, href)
            text = a.get_text().strip()
            
            if text and not text.isspace():
                links.append({
                    "text": text[:100],
                    "url": absolute_url
                })
        
        # 去重
        seen = set()
        unique_links = []
        for link in links:
            if link['url'] not in seen:
                seen.add(link['url'])
                unique_links.append(link)
        
        return unique_links[:50]
        
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
def extract_metadata(url: str) -> dict:
    """
    提取网站元数据（标题、描述、关键词、图片）
    
    Args:
        url: 要提取元数据的网站URL
        
    Returns:
        包含title、description、keywords、og_image的字典
    """
    try:
        with httpx.Client(follow_redirects=True, timeout=30, headers=HEADERS) as client:
            response = client.get(url)
            response.raise_for_status()
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 基本元数据
        title = soup.title.string.strip() if soup.title else ""
        
        description = ""
        desc_tag = soup.find('meta', attrs={'name': 'description'})
        if desc_tag:
            description = desc_tag.get('content', '')
        
        keywords = ""
        kw_tag = soup.find('meta', attrs={'name': 'keywords'})
        if kw_tag:
            keywords = kw_tag.get('content', '')
        
        # Open Graph 标签
        og_image = ""
        og_tag = soup.find('meta', attrs={'property': 'og:image'})
        if og_tag:
            og_image = og_tag.get('content', '')
        
        # 统计图片数量
        images = len(soup.find_all('img'))
        
        return {
            "title": title,
            "description": description,
            "keywords": keywords,
            "og_image": og_image,
            "image_count": images,
            "final_url": str(response.url)
        }
        
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def scrape_multiple_pages(urls: list) -> dict:
    """
    批量抓取多个页面（最多10个）
    
    Args:
        urls: 要抓取的URL列表
        
    Returns:
        每个URL对应的内容
    """
    results = {}
    for url in urls[:10]:
        results[url] = scrape_website(url)
    return results


@mcp.tool()
def find_emails_on_page(url: str) -> list:
    """
    在网站上找所有邮箱地址
    
    Args:
        url: 要搜索邮箱的网站URL
        
    Returns:
        找到的邮箱列表
    """
    try:
        with httpx.Client(follow_redirects=True, timeout=30, headers=HEADERS) as client:
            response = client.get(url)
            response.raise_for_status()
            
        # 用正则找邮箱
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, response.text)
        
        # 去重
        unique_emails = list(set(emails))
        
        return unique_emails[:20]
        
    except Exception as e:
        return [f"Error: {str(e)}"]


if __name__ == "__main__":
    mcp.run()

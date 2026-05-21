
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASE_DIR, 'data')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

DOUYIN_API_URL = "https://www.douyin.com/aweme/v1/web/search/item/"

REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Referer': 'https://www.douyin.com/',
    'Origin': 'https://www.douyin.com',
}

DEFAULT_KEYWORDS = ["手机", "笔记本电脑", "耳机"]
DEFAULT_PAGE_SIZE = 20
MAX_PAGES = 5

CHART_CONFIG = {
    'dpi': 100,
    'figsize': (12, 6),
    'font_family': 'SimHei',
    'font_size': 12,
}

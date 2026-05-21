
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASE_DIR, 'data')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

DOUYIN_API_URL = "https://www.douyin.com/aweme/v1/web/search/item/"

REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Referer': 'https://www.douyin.com/search/耳机?type=goods',
    'Cookie': 'ttwid=1; msToken=; s_v_web_id=verify_xxx;',
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

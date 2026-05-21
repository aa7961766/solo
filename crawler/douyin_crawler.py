
import json
import re
from datetime import datetime
from crawler.api_client import ApiClient
from models.product import Product
from config.settings import MAX_PAGES, DEFAULT_PAGE_SIZE
from config.douyin_config import DouyinConfig
import os

class DouyinCrawler:
    def __init__(self):
        self.client = ApiClient()
        self.config = DouyinConfig()
        
        if not self.config.is_configured():
            print("⚠️  警告：未配置抖音 Cookie，数据采集可能失败！")
            print("请运行 python -m config.setup_cookie 进行配置")
    
    def search_products(self, keyword, pages=1, page_size=DEFAULT_PAGE_SIZE):
        products = []
        base_url = "https://www.douyin.com/aweme/v1/web/search/item/"
        
        if not self.config.is_configured():
            print("❌ 错误：未配置有效的抖音 Cookie")
            print("请先运行 python -m config.setup_cookie 配置 Cookie")
            return products
        
        try:
            for page in range(pages):
                params = {
                    'keyword': keyword,
                    'count': page_size,
                    'cursor': page * page_size,
                    'type': '0',
                    'detail_list': '1',
                    'version_code': '170400',
                    'version_name': '17.4.0',
                    'cookie_enabled': 'true',
                    'screen_width': '375',
                    'screen_height': '667',
                    'browser_language': 'zh-CN',
                    'browser_platform': 'iPhone',
                    'browser_name': 'Safari',
                    'browser_version': '16.6',
                    'browser_online': 'true',
                    'engine_name': 'Webkit',
                    'engine_version': '605.1.15',
                    'os_name': 'iOS',
                    'os_version': '16.6',
                    'cpu_core_num': '6',
                    'device_memory': '4',
                    'platform': 'iOS',
                    'downlink': '10',
                    'effective_type': '4g',
                    'round_trip_time': '50',
                }
                
                if self.config.device_id:
                    params['device_id'] = self.config.device_id
                
                response = self.client.get(base_url, params=params, cookie=self.config.cookie)
                print(f"API响应状态码: {response.status_code}")
                data = response.json()
                
                if response.status_code != 200:
                    print(f"❌ API请求失败，状态码: {response.status_code}")
                    continue
                
                if self._is_empty_response(data):
                    print(f"⚠️  API返回空数据，搜索关键词: {keyword}")
                    if 'search_nil_info' in data and data['search_nil_info'].get('search_nil_item') == 'invalid_app':
                        print("❌ Cookie 无效或已过期，请更新 Cookie")
                        print("运行 python -m config.setup_cookie 更新配置")
                    continue
                
                items = self._extract_items(data)
                print(f"✓ 提取到 {len(items)} 条商品数据")
                
                for item in items:
                    product = self._parse_product(item)
                    if product:
                        products.append(product)
                
                if not items:
                    break
                    
        except Exception as e:
            print(f"❌ 搜索时出错: {e}")
            import traceback
            traceback.print_exc()
        
        if not products:
            print(f"⚠️  未采集到有效数据，搜索关键词: {keyword}")
        else:
            print(f"✓ 成功采集到 {len(products)} 条商品数据")
        
        return products
    
    def _is_empty_response(self, data):
        if not data:
            return True
        if 'search_nil_info' in data:
            return True
        items = self._extract_items(data)
        return len(items) == 0
    
    def _extract_items(self, data):
        if isinstance(data, dict):
            if 'data' in data and isinstance(data['data'], dict):
                if 'list' in data['data']:
                    return data['data']['list']
            elif 'list' in data:
                return data['list']
            elif 'aweme_list' in data:
                return data['aweme_list']
        elif isinstance(data, list):
            return data
        return []
    
    def _parse_product(self, item):
        try:
            product_info = None
            
            if isinstance(item, dict):
                if 'aweme_info' in item and 'product_info' in item['aweme_info']:
                    product_info = item['aweme_info']['product_info']
                elif 'product_info' in item:
                    product_info = item['product_info']
                elif 'product' in item:
                    product_info = item['product']
            
            if not product_info or not isinstance(product_info, dict):
                return None
            
            product_id = str(product_info.get('product_id', '')) or str(product_info.get('id', ''))
            name = product_info.get('product_name', '') or product_info.get('name', '')
            
            price_str = str(product_info.get('min_price', '0'))
            try:
                price = float(price_str) / 100 if float(price_str) > 0 else float(product_info.get('price', '0'))
            except:
                price = 0
            
            sales = self._parse_sales(product_info.get('sales', '') or product_info.get('sales_count', ''))
            shop_name = product_info.get('shop_name', '') or product_info.get('merchant_name', '')
            shop_rating = float(product_info.get('shop_score', '0')) or float(product_info.get('rating', '0'))
            
            url = f"https://www.douyin.com/product/{product_id}" if product_id else ""
            image_url = product_info.get('cover_image', '') or product_info.get('image', '')
            
            if not product_id or not name or price <= 0:
                return None
            
            return Product(
                id=product_id,
                name=name,
                price=price,
                sales=sales,
                shop_name=shop_name,
                shop_rating=shop_rating,
                url=url,
                image_url=image_url,
                crawl_time=datetime.now()
            )
        except Exception as e:
            print(f"解析商品数据时出错: {e}")
            return None
    
    def _parse_sales(self, sales_str):
        if not sales_str:
            return 0
        sales_str = str(sales_str)
        match = re.search(r'(\d+(?:\.\d+)?)', sales_str)
        if match:
            num = float(match.group(1))
            if '万' in sales_str:
                num *= 10000
            return int(num)
        return 0
    
    def close(self):
        self.client.close()

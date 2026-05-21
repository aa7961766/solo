
import json
import math
from datetime import datetime
from models.product import Product
from config.settings import DATA_DIR

class DataProcessor:
    def __init__(self):
        pass
    
    def clean_data(self, products):
        cleaned = []
        for product in products:
            if self._is_valid(product):
                cleaned.append(product)
        return cleaned
    
    def _is_valid(self, product):
        if not product.id or not product.name:
            return False
        if product.price <= 0:
            return False
        if len(product.name.strip()) < 3:
            return False
        return True
    
    def deduplicate(self, products):
        seen = set()
        unique = []
        for product in products:
            key = (product.id, product.name, product.price)
            if key not in seen:
                seen.add(key)
                unique.append(product)
        return unique
    
    def sort_by_price(self, products, ascending=True):
        return sorted(products, key=lambda p: (p.price, -p.sales), reverse=not ascending)
    
    def calculate_value_score(self, products):
        if not products:
            return products
        
        max_sales = max(p.sales for p in products) if products else 1
        
        for product in products:
            if product.price > 0 and max_sales > 0:
                log_sales = math.log(product.sales + 1)
                log_max_sales = math.log(max_sales + 1)
                normalized_sales = log_sales / log_max_sales
                value_score = (product.shop_rating / 5) * normalized_sales / (product.price / 1000)
                product.value_score = value_score
            else:
                product.value_score = 0
        return sorted(products, key=lambda p: p.value_score, reverse=True)
    
    def get_top_value_products(self, products, n=3):
        scored = self.calculate_value_score(list(products))
        return scored[:n]
    
    def save_to_file(self, products, filename=None):
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'products_{timestamp}.json'
        
        filepath = f"{DATA_DIR}/{filename}"
        data = [product.to_dict() for product in products]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return filepath
    
    def load_from_file(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return [Product.from_dict(item) for item in data]
    
    def analyze_price_distribution(self, products):
        prices = [p.price for p in products]
        if not prices:
            return {}
        
        stats = {
            'min_price': min(prices),
            'max_price': max(prices),
            'avg_price': sum(prices) / len(prices),
            'median_price': sorted(prices)[len(prices) // 2],
            'count': len(prices)
        }
        return stats

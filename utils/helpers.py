
import os
import sys

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def format_price(price):
    return f'¥{price:.2f}'

def format_sales(sales):
    if sales >= 10000:
        return f'{sales / 10000:.1f}万'
    return str(sales)

def truncate_text(text, max_length=30):
    if len(text) <= max_length:
        return text
    return text[:max_length] + '...'

def setup_path():
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

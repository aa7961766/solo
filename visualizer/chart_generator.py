
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
from config.settings import OUTPUT_DIR, CHART_CONFIG

class ChartGenerator:
    def __init__(self):
        plt.rcParams['font.family'] = CHART_CONFIG['font_family']
        plt.rcParams['font.size'] = CHART_CONFIG['font_size']
        plt.rcParams['axes.unicode_minus'] = False
    
    def generate_price_histogram(self, products, keyword):
        prices = [p.price for p in products]
        if not prices:
            return None
        
        plt.figure(figsize=CHART_CONFIG['figsize'], dpi=CHART_CONFIG['dpi'])
        plt.hist(prices, bins=20, edgecolor='black', alpha=0.7)
        plt.title(f'{keyword} - 价格分布直方图')
        plt.xlabel('价格 (元)')
        plt.ylabel('商品数量')
        plt.grid(axis='y', alpha=0.3)
        
        filepath = os.path.join(OUTPUT_DIR, f'price_hist_{keyword}.png')
        plt.savefig(filepath, bbox_inches='tight')
        plt.close()
        return filepath
    
    def generate_price_sales_scatter(self, products, keyword):
        prices = [p.price for p in products]
        sales = [p.sales for p in products]
        
        if not prices or not sales:
            return None
        
        plt.figure(figsize=CHART_CONFIG['figsize'], dpi=CHART_CONFIG['dpi'])
        plt.scatter(prices, sales, alpha=0.6, color='orange')
        plt.title(f'{keyword} - 价格与销量关系')
        plt.xlabel('价格 (元)')
        plt.ylabel('销量')
        plt.grid(alpha=0.3)
        
        filepath = os.path.join(OUTPUT_DIR, f'price_sales_{keyword}.png')
        plt.savefig(filepath, bbox_inches='tight')
        plt.close()
        return filepath
    
    def generate_value_bar_chart(self, products, keyword, top_n=10):
        top_products = products[:top_n]
        names = [p.name[:15] + '...' if len(p.name) > 15 else p.name for p in top_products]
        scores = [getattr(p, 'value_score', 0) for p in top_products]
        
        if not names or not scores:
            return None
        
        plt.figure(figsize=(12, 8), dpi=CHART_CONFIG['dpi'])
        plt.barh(names, scores, color='green')
        plt.title(f'{keyword} - 性价比排名 (Top {top_n})')
        plt.xlabel('性价比得分')
        plt.ylabel('商品名称')
        plt.grid(axis='x', alpha=0.3)
        plt.gca().invert_yaxis()
        
        filepath = os.path.join(OUTPUT_DIR, f'value_bar_{keyword}.png')
        plt.savefig(filepath, bbox_inches='tight')
        plt.close()
        return filepath
    
    def generate_comparison_table_html(self, products, keyword):
        products_sorted = sorted(products, key=lambda p: p.price)
        rows_html = ''
        
        for i, product in enumerate(products_sorted[:10], 1):
            rows_html += f'''
            <tr>
                <td>{i}</td>
                <td><a href="{product.url}" target="_blank">{product.name[:30]}...</a></td>
                <td>¥{product.price:.2f}</td>
                <td>{product.sales}</td>
                <td>{product.shop_rating}</td>
                <td>{product.shop_name}</td>
            </tr>
            '''
        
        html = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>{keyword} - 商品对比</title>
            <style>
                table {{ width: 100%; border-collapse: collapse; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                tr:nth-child(even) {{ background-color: #f9f9f9; }}
                a {{ text-decoration: none; color: #1a73e8; }}
            </style>
        </head>
        <body>
            <h1>{keyword} - 商品横向对比表</h1>
            <table>
                <tr>
                    <th>排名</th>
                    <th>商品名称</th>
                    <th>价格</th>
                    <th>销量</th>
                    <th>店铺评分</th>
                    <th>店铺名称</th>
                </tr>
                {rows_html}
            </table>
        </body>
        </html>
        '''
        
        filepath = os.path.join(OUTPUT_DIR, f'comparison_{keyword}.html')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return filepath


import subprocess
import sys
import os

def install_dependencies():
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', requirements_path])
        print('依赖安装完成')
    except subprocess.CalledProcessError as e:
        print(f'依赖安装失败: {e}')

try:
    import argparse
    from crawler.douyin_crawler import DouyinCrawler
    from processor.data_processor import DataProcessor
    from visualizer.chart_generator import ChartGenerator
    from utils.helpers import format_price, format_sales, truncate_text
except ImportError:
    print('缺少依赖，正在自动安装...')
    install_dependencies()
    import argparse
    from crawler.douyin_crawler import DouyinCrawler
    from processor.data_processor import DataProcessor
    from visualizer.chart_generator import ChartGenerator
    from utils.helpers import format_price, format_sales, truncate_text

def main():
    parser = argparse.ArgumentParser(description='电商商品价格采集与对比工具')
    parser.add_argument('-k', '--keyword', required=True, help='搜索关键词')
    parser.add_argument('-p', '--pages', type=int, default=1, help='采集页数')
    parser.add_argument('-s', '--save', action='store_true', help='保存数据到文件')
    parser.add_argument('-v', '--visualize', action='store_true', help='生成可视化图表')
    args = parser.parse_args()
    
    print(f'正在搜索关键词: {args.keyword}')
    
    crawler = DouyinCrawler()
    processor = DataProcessor()
    chart_gen = ChartGenerator()
    
    try:
        raw_products = crawler.search_products(args.keyword, pages=args.pages)
        
        if not raw_products:
            print(f'未找到关于 "{args.keyword}" 的商品数据，请尝试其他关键词')
            return
        
        print(f'原始采集到 {len(raw_products)} 条商品数据')
        
        cleaned = processor.clean_data(raw_products)
        print(f'清洗后剩余 {len(cleaned)} 条有效数据')
        
        unique = processor.deduplicate(cleaned)
        print(f'去重后剩余 {len(unique)} 条数据')
        
        sorted_products = processor.sort_by_price(unique)
        
        if args.save:
            filepath = processor.save_to_file(sorted_products)
            print(f'数据已保存到: {filepath}')
        
        print('\n商品价格从低到高排序结果:')
        print('=' * 100)
        print(f'{"排名":<4} {"名称":<40} {"价格":<10} {"销量":<10} {"评分":<6} {"店铺"}')
        print('=' * 100)
        
        for i, product in enumerate(sorted_products[:10], 1):
            print(f'{i:<4} {truncate_text(product.name, 38):<40} {format_price(product.price):<10} '
                  f'{format_sales(product.sales):<10} {product.shop_rating:<6} {product.shop_name}')
        
        print('\n性价比推荐 Top 3:')
        print('=' * 100)
        top_value = processor.get_top_value_products(sorted_products, n=3)
        for i, product in enumerate(top_value, 1):
            score = getattr(product, 'value_score', 0)
            print(f'Top{i}: {truncate_text(product.name, 40)} - 价格:{format_price(product.price)} '
                  f'- 销量:{format_sales(product.sales)} - 评分:{product.shop_rating} - 性价比:{score:.2f}')
        
        if args.visualize:
            print('\n正在生成可视化图表...')
            chart_gen.generate_price_histogram(sorted_products, args.keyword)
            chart_gen.generate_price_sales_scatter(sorted_products, args.keyword)
            chart_gen.generate_value_bar_chart(top_value, args.keyword)
            chart_gen.generate_comparison_table_html(sorted_products, args.keyword)
            print('可视化图表已生成')
        
    finally:
        crawler.close()

if __name__ == '__main__':
    main()

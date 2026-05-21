
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
    from flask import Flask, render_template, request, jsonify, send_from_directory
    from crawler.douyin_crawler import DouyinCrawler
    from processor.data_processor import DataProcessor
    from visualizer.chart_generator import ChartGenerator
except ImportError:
    print('缺少依赖，正在自动安装...')
    install_dependencies()
    from flask import Flask, render_template, request, jsonify, send_from_directory
    from crawler.douyin_crawler import DouyinCrawler
    from processor.data_processor import DataProcessor
    from visualizer.chart_generator import ChartGenerator

app = Flask(__name__, template_folder='templates')

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'output')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/crawl', methods=['POST'])
def crawl_api():
    try:
        data = request.get_json()
        keyword = data.get('keyword', '')
        
        if not keyword:
            return jsonify({'success': False, 'message': '请输入关键词'})
        
        crawler = DouyinCrawler()
        processor = DataProcessor()
        chart_gen = ChartGenerator()
        
        raw_products = crawler.search_products(keyword, pages=2)
        cleaned = processor.clean_data(raw_products)
        unique = processor.deduplicate(cleaned)
        sorted_products = processor.sort_by_price(unique)
        
        top_value = processor.get_top_value_products(sorted_products, n=3)
        top_ids = {p.id for p in top_value}
        
        for i, p in enumerate(top_value, 1):
            p.is_recommend = True
            p.recommend_rank = i
        
        for p in sorted_products:
            if p.id not in top_ids:
                p.is_recommend = False
                p.recommend_rank = 0
        
        stats = processor.analyze_price_distribution(sorted_products)
        
        chart_gen.generate_price_histogram(sorted_products, keyword)
        chart_gen.generate_price_sales_scatter(sorted_products, keyword)
        chart_gen.generate_value_bar_chart(top_value, keyword)
        chart_gen.generate_comparison_table_html(sorted_products, keyword)
        
        crawler.close()
        
        products_data = []
        for p in sorted_products[:10]:
            products_data.append({
                'id': p.id,
                'name': p.name,
                'price': p.price,
                'sales': p.sales,
                'shop_rating': p.shop_rating,
                'shop_name': p.shop_name,
                'url': p.url,
                'is_recommend': getattr(p, 'is_recommend', False),
                'recommend_rank': getattr(p, 'recommend_rank', 0)
            })
        
        return jsonify({
            'success': True,
            'keyword': keyword,
            'products': products_data,
            'stats': stats
        })
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/static/charts/<filename>')
def serve_chart(filename):
    return send_from_directory(OUTPUT_DIR, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

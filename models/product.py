
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Product:
    id: str
    name: str
    price: float
    sales: int
    shop_name: str
    shop_rating: float
    url: str
    image_url: str
    crawl_time: datetime
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'sales': self.sales,
            'shop_name': self.shop_name,
            'shop_rating': self.shop_rating,
            'url': self.url,
            'image_url': self.image_url,
            'crawl_time': self.crawl_time.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data['id'],
            name=data['name'],
            price=data['price'],
            sales=data['sales'],
            shop_name=data['shop_name'],
            shop_rating=data['shop_rating'],
            url=data['url'],
            image_url=data['image_url'],
            crawl_time=datetime.fromisoformat(data['crawl_time'])
        )

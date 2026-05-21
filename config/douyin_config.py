import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE = os.path.join(BASE_DIR, 'config', 'douyin_config.json')

class DouyinConfig:
    def __init__(self):
        self.cookie = ""
        self.device_id = ""
        self.load()
    
    def load(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.cookie = data.get('cookie', '')
                    self.device_id = data.get('device_id', '')
            except:
                pass
    
    def save(self, cookie=None, device_id=None):
        data = {
            'cookie': cookie or self.cookie,
            'device_id': device_id or self.device_id
        }
        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        self.cookie = data['cookie']
        self.device_id = data['device_id']
    
    def is_configured(self):
        return bool(self.cookie and 'odin_tt' in self.cookie)

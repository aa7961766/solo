
import requests
import time
import random
from config.settings import REQUEST_HEADERS

class ApiClient:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(REQUEST_HEADERS)
        self.delay = 1.5
        self.max_retries = 3
    
    def get(self, url, params=None, timeout=10, cookies=None):
        for retry in range(self.max_retries):
            try:
                response = self.session.get(url, params=params, cookies=cookies, timeout=timeout)
                response.raise_for_status()
                response.encoding = response.apparent_encoding
                time.sleep(self.delay + random.uniform(0.5, 1.5))
                return response
            except requests.exceptions.RequestException as e:
                if retry < self.max_retries - 1:
                    time.sleep(2 ** retry)
                    continue
                raise e
    
    def post(self, url, data=None, json=None, timeout=10, cookies=None):
        for retry in range(self.max_retries):
            try:
                response = self.session.post(url, data=data, json=json, cookies=cookies, timeout=timeout)
                response.raise_for_status()
                response.encoding = response.apparent_encoding
                time.sleep(self.delay + random.uniform(0.5, 1.5))
                return response
            except requests.exceptions.RequestException as e:
                if retry < self.max_retries - 1:
                    time.sleep(2 ** retry)
                    continue
                raise e
    
    def close(self):
        self.session.close()

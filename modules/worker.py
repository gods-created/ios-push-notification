from bs4 import BeautifulSoup as bs
from os import getenv
import aiohttp
import copy
import webbrowser

class Singleton(type):
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
            
        return cls._instance

class Worker(metaclass=Singleton):
    base_url = getenv('BASE_URL')
            
    def __init__(self):
        self.st_response = {'status': 'error', 'err_description': ''}
        self.replace_elems = {'$': '', ',': ''}
        
    @classmethod
    def open_browser(cls) -> None:
        webbrowser.open_new(cls.base_url)
        
    async def __aenter__(self, *args, **kwargs):
        return self
        
    async def __get_current_price(self, html: str) -> dict:
        response_json = copy.deepcopy(self.st_response)
        
        try:
            replace_elems = self.replace_elems
            soup = bs(html, 'html.parser')
            price, *_ = soup.find_all('span', {'data-test': 'text-cdp-price-display'})
            price = price.get_text()
            
            for key in replace_elems.keys():
                value = replace_elems[key]
                price = price.replace(key, value)
            
            response_json['price'] = float(price)
            response_json['status'] = 'success'
            
        except Exception as e:
            response_json['err_description'] = str(e)
            
        finally:
            return response_json
        
    async def executing(self) -> dict:
        response_json = copy.deepcopy(self.st_response)
        
        try:
            url = self.base_url
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers={}) as request:
                    status = request.status
                    if status not in [200, 201]:
                        response_json['err_description'] = f'API request failed! Status code is {status}.'
                        return response_json
                        
                    html = await request.text()
                    
            current_price_response = await self.__get_current_price(html)
            response_json = copy.copy(current_price_response)
            
        except Exception as e:
            response_json['err_description'] = str(e)
            
        finally:
            return response_json
        
    async def __aexit__(self, *args, **kwargs):
        pass

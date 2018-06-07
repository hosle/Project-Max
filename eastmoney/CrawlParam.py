"""
Created on 18/6/7
@Author hosle 
Original@ AIStock
"""
__all__ = ['CrawlParam']


class CrawlParam:
    def __init__(self, _cookie_dict, _token):
        self.cookie = _cookie_dict
        self.token = _token

"""
Created on 18/6/7
@Author hosle 
Original@ AIStock
"""
import requests
import datetime
import time
import os
import pathlib
import json

from util import file_util
from eastmoney import CrawlParam


def fetch_all_rzrq(_stock_code, _max_page, _crawl_param):
    print('start crawling rzrq data!')
    _crawl_param = get_common_param(_stock_code, _crawl_param)

    path = os.getcwd() + '/data/eastmoney_rzrq/'
    file = path + '{:s}.txt'.format(_stock_code)

    result_list = []
    res_json = do_crawl(_crawl_param)
    result_list.extend(res_json['result'])
    print("result length = {:d}".format(len(result_list)))

    page_count = 1
    page_total = min(res_json['TotalPage'], _max_page)

    while page_count < page_total:
        page_count += 1
        _crawl_param.url_param['page'] = page_count
        print("page ={:d}".format(_crawl_param.url_param['page']))
        res_json = do_crawl(_crawl_param)
        result_list.extend(res_json['result'])
        print("update result length to {:d} by page {:d}".format(len(result_list), page_count))

    file_util.update_to_file(path, file, json.dumps(result_list))


def get_common_param(_stock_code, _crawl_param):
    _crawl_param.stock_code = _stock_code
    _crawl_param.url = 'http://m.data.eastmoney.com/Rzrq/GetRzrqList_xq'

    _crawl_param.url_param = {
                 'page': 1,
                 'pagesize': 20,
                 'code': _stock_code}

    return _crawl_param


def do_crawl(_crawl_param):
    url = _crawl_param.url

    headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, "
                          "like Gecko) Mobile/15E216 color=d eastmoney_ios appversion_7.4",
            'Host': 'm.data.eastmoney.com',
            'Accept-Language': 'zh-tw',
            'Accept-Encoding': 'gzip, deflate',
            'Refer': 'http://m.data.eastmoney.com/rzrq/detail,{:s}.html'.format(_crawl_param.stock_code),
            'X-Requested-With': 'XMLHttpRequest',
            'Accept': 'application/json, text/javascript, */*; q=0.01'

        }
    res = requests.get(url, headers=headers, cookies=_crawl_param.cookie, params=_crawl_param.url_param)
    # print(res.url)

    if res.status_code != 200:
            return False
    print(res.status_code)
    res_json = res.json()

    return res_json


if __name__ == '__main__':
    cookie = dict(_ga='GA1.2.468211723.1528164067', _gid='GA1.2.759505654.1528164067', st_si='86370669874472',
                  st_pvi='31108259223879', appinfo='ios%5E-%5Eeastmoney%3A//wireless/txtrade/originTradeLogin')
    crawl_param = CrawlParam(cookie, '')

    fetch_all_rzrq('000333',2, crawl_param)

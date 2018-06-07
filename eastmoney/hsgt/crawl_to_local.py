"""
Created on 18/6/5
@Author hosle
Original@ AIStock
"""

import requests
import datetime
import time
import os
import pathlib
import json


__all__ = ['CrawlParam', 'fetch_data']


class CrawlParam:
    def __init__(self, _cookie_dict, _token):
        self.cookie = _cookie_dict
        self.token = _token


def fetch_all_data(_stock_code, _stock_type, _crawl_param):
    path = os.getcwd() + '/data/eastmoney_hsgt/'
    file = path + '{:s}.txt'.format(_stock_code)

    result_list = []
    res_json = fetch_data(_stock_code, _stock_type, _crawl_param)
    result_list.extend(res_json['result'])
    print("result length = {:d}".format(len(result_list)))

    page_count = 1
    page_total = res_json['TotalPage']

    while page_count < page_total:
        page_count += 1
        _crawl_param.url_param['p'] = page_count
        _crawl_param.url_param['page'] = page_count

        res_json = fetch_data(_stock_code, _stock_type, _crawl_param)
        result_list.extend(res_json['result'])
        print("update result length to {:d} by page {:d}".format(len(result_list), page_count))

    save_in_disk(path, file, json.dumps(result_list))


def fetch_data(_stock_code, _stock_type, _crawl_param):
    # _crawl_param.dir_name = 'eastmoney_hsgt/'
    # _crawl_param.file_name = _stock_code
    _crawl_param.stock_code = _stock_code
    _crawl_param.url = 'https://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get'

    url_param = {'_': int(round(time.time() * 1000)),
                 'type': 'HSGTCJB',
                 'cmd': _stock_code,
                 'st': 'DetailDate',
                 'sr': -1,
                 'p': 1,
                 'page': 1,
                 'pagesize': 20,
                 'ps': 20,
                 'token': _crawl_param.token,
                 'sty': _stock_type,
                 # 'callback': '',
                 'js': '''{"result":(x),"TotalPage":(tp)}'''}

    _crawl_param.url_param = url_param

    ##get each
    return do_grab(_crawl_param)


def do_grab(crawl_param):
    url = crawl_param.url

    headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, "
                          "like Gecko) Mobile/15E216 color=d eastmoney_ios appversion_7.4",
            'Host': 'dcfm.eastmoney.com',
            'Accept-Language': 'zh-tw',
            'Accept-Encoding': 'br, gzip, deflate',
            'Refer': 'http://m.data.eastmoney.com/hsgt/detail/{:s}'.format(crawl_param.stock_code),
            'Accept': '*/*',
        }
    res = requests.get(url, headers=headers, cookies=crawl_param.cookie, params=crawl_param.url_param)
    # print(res.url)

    if res.status_code != 200:
            return False
    print(res.status_code)
    res_json = res.json()

    return res_json


    # path = os.getcwd() + '/data/{:s}'.format(crawl_param.dir_name)
    # file = path + '{:s}.txt'.format(crawl_param.file_name)
    #
    # save_in_disk(path, file, res.text)


def update_to_file(_path, _filename, _content):

    path = pathlib.Path(_path)
    file = pathlib.Path(_filename)

    if file.exists() and file.is_file():
        _mode = 'a'
    else:
        _mode = 'w'

        if not path.exists():
            path.mkdir()
        file.touch()
    with open(_filename, _mode) as f:
        f.write(_content)


def get_now_date():
    date = datetime.datetime.now()
    return date.strftime('%Y%m%d')


def save_in_disk(path, filename, content):
        if not os.path.exists(path):
            os.makedirs(path)
        with open(filename, 'w') as f:
            f.write(content)


if __name__ == '__main__':

    cookie = dict(_ga='GA1.2.468211723.1528164067', _gat='1', _gid='GA1.2.759505654.1528164067', st_si='76042854848500', st_pvi='31108259223879')
    token = '70f12f2f4f091e459a279469fe49eca5'
    crawl_param = CrawlParam(cookie, token)

    fetch_data('000333', 'sgt', crawl_param)
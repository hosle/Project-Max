"""
Created on 18/5/26
@Author hosle 
Original@ AIStock
"""

import requests
import datetime
import os

__all__ = ['GrabParam', 'fetch_all_hgtb', 'fetch_all_sgtb']


class GrabParam:
    def __init__(self, my_cookie):
        self.cookie = dict(v=my_cookie)


def fetch_all_hgtb(_from, _to, grab_param):
    grab_param.dir_name = get_now_date() + '/hgtb/'
    grab_param.file_name = 'hgtb'
    grab_param.url_prefix = 'http://data.10jqka.com.cn/hgt/hgtb/field/zdf/order/desc/ajax/1/page/'
    grab_param.url_suffix = '/'

    for i in range(_from, _to):
        do_grab(grab_param, i + 1)


def fetch_all_sgtb(_from, _to, grab_param):
    grab_param.dir_name = get_now_date() + '/sgtb/'
    grab_param.file_name = 'sgtb'
    grab_param.url_prefix = 'http://data.10jqka.com.cn/hgt/sgtb/field/zdf/order/desc/page/'
    grab_param.url_suffix = '/ajax/1/'

    for i in range(_from, _to):
        do_grab(grab_param, i + 1)


def do_grab(grab_param, i):
    url = grab_param.url_prefix + str(i) + grab_param.url_suffix

    headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
            'Host': 'data.10jqka.com.cn',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Upgrade-Insecure-Requests': '1'
        }

    res = requests.get(url, headers=headers, cookies=grab_param.cookie)

    if res.status_code != 200:
            return False
    print(res.status_code)

    path = os.getcwd() + '/data/{:s}'.format(grab_param.dir_name)
    file = path + '{:s}{:d}.txt'.format(grab_param.file_name, i)

    save_in_disk(path, file, res.text)


def get_now_date():
    date = datetime.datetime.now()
    return '{:d}{:0>2d}{:d}'.format(date.year, date.month, date.day)


def fetch_sgtb(date, i):
        url_prefix = 'http://data.10jqka.com.cn/hgt/sgtb/field/zdf/order/desc/page/'
        url_suffix = '/ajax/1/'

        url = url_prefix + str(i) + url_suffix

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
            'Host': 'data.10jqka.com.cn',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Upgrade-Insecure-Requests': '1'
        }
        cookie = dict(v='AtUmPHcmIhIypwZuM7-k1u_-4tqL0onkU4ZtOFd6kcybrvsMHyKZtOPWfx7k')

        res1 = requests.get(url, headers=headers, cookies=cookie)

        if res1.status_code != 200:
            return False

        print(res1.status_code)
        with open('../data/{:s}/sgtb/sgtb{:d}'.format(date, i), 'w') as f:
            f.write(res1.text)


def save_in_disk(path, filename, content):
        if not os.path.exists(path):
            os.makedirs(path)
        with open(filename, 'w') as f:
            f.write(content)


if __name__ == '__main__':
    _cookieString = 'Ai3exJ-eCoVIz-5pyGN8Xkc2OsKjimFG677FMG8yaUQz5kM0N9pxLHsOw5v8'
    # fetchAllHgtb('0524')
    fetch_all_hgtb('0525', _cookieString)

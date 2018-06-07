import numpy as np
import matplotlib.pyplot as plt
import pandas
import json

import eastmoney


def crawl_hsgt(_stock_code):
    cookie = dict(_ga='GA1.2.468211723.1528164067', _gat='1', _gid='GA1.2.759505654.1528164067', st_si='76042854848500',
                  st_pvi='31108259223879')
    token = '70f12f2f4f091e459a279469fe49eca5'
    crawl_param = eastmoney.CrawlParam(cookie, token)

    eastmoney.fetch_all_hsgt(_stock_code, 'sgt', crawl_param)


def read_hsgt_json(_stock_code):
    _file_name = 'data/eastmoney_hsgt/{:s}.txt'.format(_stock_code)
    with open(_file_name) as f:
        _data = json.load(f)

    _data_df = pandas.DataFrame(_data)
    _data_df.set_index('DetailDate', inplace=True)
    _data_df.index = pandas.DatetimeIndex(_data_df.index)
    _data_df = _data_df.drop_duplicates()
    return _data_df


def crawl_rzrq(_stock_code):
    cookie = dict(_ga='GA1.2.468211723.1528164067', _gid='GA1.2.759505654.1528164067', st_si='86370669874472',
                  st_pvi='31108259223879', appinfo='ios%5E-%5Eeastmoney%3A//wireless/txtrade/originTradeLogin')
    crawl_param = eastmoney.CrawlParam(cookie, '')

    eastmoney.fetch_all_rzrq('000333', 2, crawl_param)


def read_rzrq_json(_stock_code):
    _file_name = 'data/eastmoney_rzrq/{:s}.txt'.format(_stock_code)
    with open(_file_name) as f:
        _data = json.load(f)

    _data_df = pandas.DataFrame(_data)
    _data_df.set_index('NoticeDate', inplace=True)
    _data_df.index = pandas.DatetimeIndex(_data_df.index)
    _data_df = _data_df.drop_duplicates()
    return _data_df


if __name__ == '__main__':

    stock_code = '000333'
    # crawl_rzrq(stock_code)

    # crawl_hsgt(stock_code)
    # data_df = read_hsgt_json(stock_code)
    # data_df_past_30day = data_df.iloc[:30, :].sort_index(ascending=True)
    # price_series = data_df_past_30day.loc[:, 'Close']
    # series2 = data_df_past_30day.loc[:, 'SGTJME']
    #
    #

    data_rzrq_df = read_rzrq_json(stock_code).iloc[:30, :].sort_index(ascending=True)
    series2 = data_rzrq_df.loc[:, 'RqylSum'].astype(float)
    price_series = data_rzrq_df.loc[:, 'Close'].astype(float)
    # print(series2)
    # print(price_series)
    length = len(price_series)


    # # #--- plotting ---
    fig, ax1 = plt.subplots()
    #
    x_tick = np.arange(length, step=3)
    plt.xticks(x_tick)
    #
    # ax1.title(stock_code)
    ax1.plot(price_series)
    ax1.set_ylabel('price', color='b')
    #
    ax2 = ax1.twinx()
    ax2.plot(series2, 'r')
    ax2.set_ylabel('rq', color='r')
    #
    fig.tight_layout()
    plt.grid(True)
    plt.show()
    # # print(price_series)
    # print("价格和深股通净买额相关系数:{:.4f}".format(np.around(jme_series.corr(price_series), decimals=4)))
    print("价格和融券相关系数:{:.4f}".format(np.around(series2.corr(price_series), decimals=4)))
    #


import hsgt

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib.font_manager import FontProperties
import pandas
import datetime
import scipy.stats as stats
from sklearn.preprocessing import StandardScaler
from bs4 import BeautifulSoup
import json

from eastmoney import crawl_to_local as crawl_eastmoney


if __name__ == '__main__':
    print()


    #--- crawl data---

    # cookie = dict(_ga='GA1.2.468211723.1528164067', _gat='1', _gid='GA1.2.759505654.1528164067', st_si='76042854848500',
    #               st_pvi='31108259223879')
    # token = '70f12f2f4f091e459a279469fe49eca5'
    # crawl_param = crawl_eastmoney.CrawlParam(cookie, token)
    #
    # crawl_eastmoney.fetch_data('000651', 'sgt', crawl_param)

    #--- read local json---
    file_name = 'data/eastmoney_hsgt/{:s}.txt'.format('000651')
    with open(file_name) as f:
        data = json.load(f)

    data_df = pandas.DataFrame(data['result'])

    price_series = data_df.loc[::-1, 'Close']
    length = len(price_series)
    price_series = price_series.rename(lambda x: length - 1 - x)
    jme_series = data_df.loc[::-1, 'SGTJME'].rename(lambda x:length - 1 - x)

    #--- plotting ---
    fig, ax1 = plt.subplots()

    x_tick = np.arange(len(price_series))
    plt.xticks(x_tick)

    ax1.plot(price_series)
    ax1.set_ylabel('price', color='b')

    ax2 = ax1.twinx()
    ax2.plot(jme_series, 'r')
    ax2.set_ylabel('Inflow Fund', color='r')

    fig.tight_layout()
    plt.grid(True)
    plt.show()
    # print(price_series)
    print("价格和深股通净买额相关系数:{:.4f}".format(np.around(jme_series.corr(price_series), decimals=4)))


    #---- plot the pearson relationship----

    # x = np.linspace(0, 360, 50)
    # y1 = np.sin(x * np.pi / 180)
    # y2 = np.sin((x / 180 + 0.5) * np.pi)
    #
    # y2_offset = np.concatenate((np.zeros(10), y2))[:50]
    #
    # p_y12 = stats.pearsonr(y1, y2)[0]
    # p_y12offset = stats.pearsonr(y1, y2_offset)[0]
    #
    # plt.plot(x, y1)
    # plt.plot(x, y2, 'r--')
    # plt.plot(x, y2_offset, 'y--')
    #
    # plt.grid(True)
    # # plt.show()
    #
    # y1_s = pandas.Series(y1)
    # y2_s = pandas.Series(y2)
    # y2_offset_s = pandas.Series(y2_offset)
    # print(np.around(y1_s.corr(y2_offset_s), decimals=4))
    #
    # print("pearsonr y1 & y2 : {:.4f}".format(np.around(p_y12, decimals=4)))
    # print("pearsonr y1 & y2_offset : {:.4f}".format(np.around(p_y12offset, decimals=4)))
    #


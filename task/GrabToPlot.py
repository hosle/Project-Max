
import hsgt

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib.font_manager import FontProperties
import pandas
import datetime

from bs4 import BeautifulSoup

count_hgtb = 11
count_sgtb = 17


def grab_data_hsgt():
    _cookie = 'AoSxZQzCg3i1tje0_TT-0IAmUwl1najFasM8JZ4lEpwQ0io_xq14l7rRDNjt'

    global count_hgtb
    global count_sgtb
    grab_param = hsgt.GrabParam(_cookie)

    hsgt.fetch_all_hgtb(8, count_hgtb, grab_param)
    # hsgt.fetch_all_sgtb(13, count_sgtb, grab_param)


def update_all_organized_data(_date_string):
    global count_hgtb
    global count_sgtb

    file_names = []
    for i_hgtb in range(1, count_hgtb + 1):
        file_names.append('data/{:s}/hgtb/hgtb{:d}.txt'.format(_date_string, i_hgtb))
    for i_sgtb in range(1, count_sgtb + 1):
        file_names.append('data/{:s}/sgtb/sgtb{:d}.txt'.format(_date_string, i_sgtb))

    for file in file_names:
        update_organized_data(file)


def update_organized_data(file_name):
    # file_name = 'data/20180528/sgtb/sgtb3.txt'
    organize_param = hsgt.OrganizeParam(file_name, lambda x: datetime.datetime.strptime(x.split('/')[1], '%Y%m%d'))
    result_tuple = hsgt.clean_up_data(organize_param)

    result_df = pandas.DataFrame(result_tuple[1], columns=result_tuple[0])
    new_stock_nums = []
    hsgt.collected_by_stock_num(result_df, lambda x: new_stock_nums.append(x))
    print("update stock nums in {:s}:{:s} ".format(file_name, str(new_stock_nums)))


def test_plot():
    x = np.linspace(0, 1)
    y = np.sin(4 * np.pi * x) * np.exp(-5 * x)
    plt.plot(x, y, 'o')
    plt.show()


def read_stock_data(_stock_num):
    return pandas.read_csv('../data/hsgt_history_by_stock/{:s}.csv'.format(_stock_num), header=0, index_col=0,
                           dtype={'股票代码': str})


def unit_yi_to_10_thousand(x):
    if not isinstance(x, str):
        return x

    trans_map = {'亿': 10 ** 4, '万': 1}
    unit_string = x[-1]

    if unit_string in trans_map.keys():
        return float(x[:-1]) * trans_map.get(unit_string)
    else:
        return x


def plot_price_fundflow(_plot_stock_num):
    font = FontProperties(fname='/Library/Fonts/Songti.ttc',
                          size=10)

    stock_df = read_stock_data(_plot_stock_num)

    format_stock_df = stock_df.drop_duplicates().applymap(unit_yi_to_10_thousand)

    stock_num = format_stock_df.iat[0, 0]
    stock_name = format_stock_df.iat[0, 1]
    series_latest_price = format_stock_df.iloc[:, 2]
    series_funds_inflow = format_stock_df.iloc[:, 9]
    series_exchange_rate = format_stock_df.iloc[:, -1]

    # print(series_latest_price)
    # print(series_funds_inflow)

    plt.figure()
    plt.subplot(311)
    plt.title('{:s}{:s}'.format(stock_num, stock_name), fontproperties=font)

    plt.ylabel(series_latest_price.name, fontproperties=font)
    plt.plot(series_latest_price)
    plt.grid(True)

    plt.subplot(312)
    plt.ylabel(series_funds_inflow.name, fontproperties=font)
    plt.plot(series_funds_inflow)
    plt.grid(True)

    plt.subplot(313)
    plt.ylabel(series_exchange_rate.name, fontproperties=font)
    plt.plot(series_exchange_rate)
    plt.grid(True)
    plt.show()


if __name__ == '__main__':

    # [step 1] :  Grab data
    #  grab_data_hsgt()

    # [step 2] : Organized Data
    # update_all_organized_data('20180531')

    # [step 3] : plotting
    stock_i_want = ['000333', '000651', '600887']
    for each_num in stock_i_want:
        plot_price_fundflow(each_num)



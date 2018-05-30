
import hsgt

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib.font_manager import FontProperties
import pandas
import datetime

from bs4 import BeautifulSoup



def grab_data_hsgt():
    _cookie = 'AqeSnEsTsLBGIDQ87beqovilMNB1LHu31QP_gnkUwQJcm8mGgfwLXuXQj9aK'

    grab_param = hsgt.GrabParam(_cookie)

    hsgt.fetch_all_hgtb(11, 12, grab_param)
    # hsgt.fetch_all_sgtb(16, 17, grab_param)


def update_all_organized_data():
    file_names = []
    for i_hgtb in range(1, 13):
        file_names.append('data/20180530/hgtb/hgtb{:d}.txt'.format(i_hgtb))
    for i_sgtb in range(1, 18):
        file_names.append('data/20180530/sgtb/sgtb{:d}.txt'.format(i_sgtb))

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
    return pandas.read_csv('data/hsgt_history_by_stock/{:s}.csv'.format(_stock_num), header=0, index_col=0,
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



if __name__ == '__main__':
    # plt.rcParams['font.family']=['simsun']


    # [step 1] :  Grab data
    #  grab_data_hsgt()

    # [step 2] : Organized Data
    # update_all_organized_data()

    # [step 3] : Analysis
    font = FontProperties(fname='/Library/Fonts/Songti.ttc',
                          size=10)

    stock_df = read_stock_data('000333')

    format_stock_df = stock_df.applymap(unit_yi_to_10_thousand)

    plot_stock_df = format_stock_df.iloc[:, [2, 9]]
    print(plot_stock_df)

    plt.figure()
    series1 = plot_stock_df.iloc[:, 0]
    series2 = plot_stock_df.iloc[:, 1]

    print(series1)
    print(series2)

    plt.figure()
    plt.subplot(211)
    plt.title('000333美的集团', fontproperties=font)
    plt.xlabel('时间', fontproperties=font)
    plt.ylabel(series1.name, fontproperties=font)
    plt.plot(series1)

    plt.subplot(212)
    plt.ylabel(series2.name, fontproperties=font)
    plt.plot(series2)

    plt.grid(True)
    plt.show()



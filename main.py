
import hsgt

import numpy as np
import matplotlib.pyplot as plt
import pandas
import datetime

from bs4 import BeautifulSoup


def grab_data_hsgt():
    _cookie = 'AhgtoXC-9_aobttyJTsNBwPg702uAXyL3mVQD1IJZNMG7bZ7-hFMGy51IJ6h'

    grab_param = hsgt.GrabParam(_cookie)

    # hsgt.fetch_all_hgtb(8, 12, grab_param)
    hsgt.fetch_all_sgtb(14, 17, grab_param)


def update_all_organized_data():
    file_names = []
    for i_hgtb in range(1, 13):
        file_names.append('data/20180529/hgtb/hgtb{:d}.txt'.format(i_hgtb))
    for i_sgtb in range(1, 18):
        file_names.append('data/20180529/sgtb/sgtb{:d}.txt'.format(i_sgtb))

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


def read_stock_data():
    stock_df = pandas.read_csv('data/hsgt_history_by_stock/000333.csv', header=0, index_col=0,
                               dtype={'股票代码': str})
    print(stock_df)


if __name__ == '__main__':
    # [step 1] :  Grab data
    #  grab_data_hsgt()
    # test_plot()

    # [step 2] : Organized Data
    # update_organized_data()
    # update_all_organized_data()

    # [step 3] : Analysis
    read_stock_data()




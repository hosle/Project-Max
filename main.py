
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


if __name__ == '__main__':
    print()


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


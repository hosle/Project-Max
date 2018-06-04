
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
    x = np.linspace(0, 360, 50)
    y1 = np.sin(x * np.pi / 180)
    y2 = np.sin((x / 180 + 0.5) * np.pi)

    plt.plot(x, y1)
    plt.plot(x, y2, 'r--')

    plt.grid(True)
    plt.show()

    p_y12 = stats.pearsonr(y1, y2)[0]

    print(np.around(p_y12, decimals=4))
    # y1_y2_df = pandas.DataFrame([y1, y2])

    # print(y1_y2_df.corr())



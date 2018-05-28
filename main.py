
import hsgt

import numpy as np
import matplotlib.pyplot as plt
import pandas
import datetime

from bs4 import BeautifulSoup


def grab_data_hsgt():
    _cookie = 'AmJXz95sTbb3BVHqHUmnAQXStePAs2YJGLVb0qz4j4iBoQxVlEO23ehHqgJ_'

    grabParam = hsgt.GrabParam(_cookie)

    hsgt.fetch_all_hgtb(10, 12, grabParam)
    # hsgt.fetch_all_sgtb(14, 17, grabParam)


def test_plot():
    x = np.linspace(0, 1)
    y = np.sin(4 * np.pi * x) * np.exp(-5 * x)
    plt.plot(x, y, 'o')
    plt.show()


def format_one_line(line_tds):
    line_array = []
    for td_j in range(1, len(line_tds)):
        line_array.append(str(line_tds[td_j].string))
    return line_array


def format_column_name(line_tds):
    line_array = []
    for td_j in range(1, len(line_tds)):
        _soup_td = BeautifulSoup(str(line_tds[td_j]), "html.parser")

        if sum(1 for x in _soup_td.descendants) > 3:
            content = str(_soup_td.a.get_text("", "<br/>"))
        else:
            content = str(_soup_td.get_text())
        line_array.append(content)
    return line_array


def clean_up_data():
    date_string = datetime.date(2018, 5, 28).strftime("%Y-%m-%d")

    with open('data/20180528/sgtb/sgtb3.txt', 'r') as f:
        html_data = f.read()
    soup_data = BeautifulSoup(html_data, 'lxml')
    line_tr = soup_data.find_all('tr')

    column_array = ['日期']
    line_array = []
    for tr_i in range(0, len(line_tr)):
        _soup_tds = BeautifulSoup(str(line_tr[tr_i]), "html.parser")

        if tr_i == 0:
            line_ths = _soup_tds.find_all('th')
            column_array.extend(format_column_name(line_ths))
        else:
            line_tds = _soup_tds.find_all('td')

            _line_data = [date_string]+format_one_line(line_tds)
            line_array.append(_line_data)

    line_series = np.array(line_array)

    return column_array, line_series





if __name__ == '__main__':
    result_tuple = clean_up_data()
    result_df = pandas.DataFrame(result_tuple[1], columns=result_tuple[0])
    print(result_df)

    # grab_data_hsgt()
    # test_plot()


"""
Created on 18/5/29
@Author hosle 
Original@ AIStock
"""

import numpy as np
import pandas
import datetime
import pathlib
from bs4 import BeautifulSoup

__all__ = ['clean_up_data', 'collected_by_stock_num', 'OrganizeParam']


class OrganizeParam:
    def __init__(self, _ori_file_name, _fun_date_time):
        self.file_name = _ori_file_name
        self.date_time = _fun_date_time(_ori_file_name)


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


def clean_up_data(_organize_param):
    _relative_file_path = _organize_param.file_name
    _date_string = _organize_param.date_time.strftime("%Y-%m-%d")

    with open(_relative_file_path, 'r') as f:
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

            _line_data = [_date_string]+format_one_line(line_tds)
            line_array.append(_line_data)

    line_series = np.array(line_array)

    return column_array, line_series


def update_to_csv(_path, filename, _content_df, _save_fun):

    path = pathlib.Path(_path)
    file = pathlib.Path(_path + filename + '.csv')

    if file.exists() and file.is_file():
        _mode = 'a'
        _header = False
    else:
        _mode = 'w'
        _header = True
        _save_fun(filename)

        if not path.exists():
            path.mkdir()
        file.touch()

    _content_df.to_csv(file, mode=_mode, header=_header, index=False, encoding='utf_8_sig')


def collected_by_stock_num(_result_df, save_fun):

    for i in range(0, len(_result_df)):
        _i_df = _result_df.loc[[i]]
        _stock_num = str(_i_df.iat[0, 1])
        # save_fun(_stock_num)
        update_to_csv('data/hsgt_history_by_stock/', '{:s}'.format(_stock_num), _i_df, save_fun)


if __name__ == '__main__':

    file_name = 'data/20180527/sgtb/sgtb3.txt'
    organize_param = OrganizeParam(file_name, lambda x: datetime.datetime.strptime(x.split('/')[1], '%Y%m%d'))
    result_tuple = clean_up_data(organize_param)

    result_df = pandas.DataFrame(result_tuple[1], columns=result_tuple[0])
    new_stock_nums = []
    collected_by_stock_num(result_df, lambda x: new_stock_nums.append(x))
    print(new_stock_nums)

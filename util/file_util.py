"""
Created on 18/6/7
@Author hosle 
Original@ AIStock
"""
import pathlib
import os

__all__ = ['update_to_file', 'save_in_disk']


def update_to_file(_path, _filename, _content):

    path = pathlib.Path(_path)
    file = pathlib.Path(_filename)

    if file.exists() and file.is_file():
        _mode = 'a'
    else:
        _mode = 'w'

        if not path.exists():
            path.mkdir()
        file.touch()
    with open(_filename, _mode) as f:
        f.write(_content)


def save_in_disk(path, filename, content):
        if not os.path.exists(path):
            os.makedirs(path)
        with open(filename, 'w') as f:
            f.write(content)

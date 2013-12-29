#!/usr/bin/env python
#
# Asynchronous using Python's ThreadPool and requests.
# UNSTABLE

import sys
from multiprocessing.pool import ThreadPool
import threading

import requests
from PySide import QtGui

from url import DOWNLOAD_URL
from window import DisplayWidget
from html_parser import parse_html


def download_data():
    print('task thread is:', threading.current_thread())
    response = requests.get(DOWNLOAD_URL)
    parse_html()
    return response.text


class MyWidget(DisplayWidget):
    def __init__(self, parent=None):
        super(MyWidget, self).__init__(parent)
        self._thread_pool = ThreadPool()

    def _button_clicked(self):
        print('gui thread is:', threading.current_thread())
        self._thread_pool.apply_async(
            download_data, [], {}, self._populate_textarea)

    def _populate_textarea(self, text):
        print('callback thread is:', threading.current_thread())
        self._textarea.setPlainText(text)


def main(argv):
    app = QtGui.QApplication(argv)
    w = MyWidget()
    w.show()
    w.raise_()
    return app.exec_()


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))

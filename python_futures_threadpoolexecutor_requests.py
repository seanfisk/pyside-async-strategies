#!/usr/bin/env python
#
# Asynchronous using the Python futures module's ThreadPoolExecutor and
# requests.
# UNSTABLE

import sys
from futures import ThreadPoolExecutor

import requests
from PySide import QtGui

from url import DOWNLOAD_URL
from window import DisplayWidget
from html_parser import parse_html


def download_data():
    response = requests.get(DOWNLOAD_URL)
    parse_html()
    return response.text


class MyWidget(DisplayWidget):
    def __init__(self, parent=None):
        super(MyWidget, self).__init__(parent)
        self._executor = ThreadPoolExecutor(max_workers=4)

    def _button_clicked(self):
        future = self._executor.submit(download_data)
        future.add_done_callback(self._populate_textarea)

    def _populate_textarea(self, future):
        self._textarea.setPlainText(future.result())


def main(argv):
    app = QtGui.QApplication(argv)
    w = MyWidget()
    w.show()
    w.raise_()
    return app.exec_()


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))

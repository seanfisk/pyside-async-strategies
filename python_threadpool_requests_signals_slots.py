#!/usr/bin/env python
#
# Asynchronous using Python's ThreadPool and requests.
#
# Pros:
# - Uses requests, so requires minimal changes to API.
# - Allows offloading HTML parsing from GUI thread, which admittedly, takes a
#   negligble amount of time.
# - Easy management of threads using the pool.
#
# Cons:
# - Uses threads when not strictly necessary.

import sys
from multiprocessing.pool import ThreadPool

import requests
from PySide import QtCore, QtGui

from url import DOWNLOAD_URL
from window import DisplayWidget
from html_parser import parse_html


class DownloadData(QtCore.QObject):
    finished = QtCore.Signal(str)

    def __call__(self):
        response = requests.get(DOWNLOAD_URL)
        parse_html()
        self.finished.emit(response.text)


class MyWidget(DisplayWidget):
    def __init__(self, parent=None):
        super(MyWidget, self).__init__(parent)

        self._thread_pool = ThreadPool()

    def _button_clicked(self):
        runnable = DownloadData()
        runnable.finished.connect(self._populate_textarea)
        self._thread_pool.apply_async(runnable)

    def _populate_textarea(self, text):
        self._textarea.setPlainText(text)


def main(argv):
    app = QtGui.QApplication(argv)
    w = MyWidget()
    w.show()
    w.raise_()
    return app.exec_()


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))

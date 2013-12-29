#!/usr/bin/env python
#
# Asynchronous using Python's (process) Pool and requests.
# DOES NOT WORK

import sys
from multiprocessing import Pool

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

        self._process_pool = Pool()

    def _button_clicked(self):
        runnable = DownloadData()
        runnable.finished.connect(self._populate_textarea)
        self._process_pool.apply_async(runnable)

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

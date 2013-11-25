#!/usr/bin/env python
#
# Asynchronous support using QThread and requests.
#
# Pros:
# - Uses requests, so requires minimal changes to API.
# - Allows offloading HTML parsing from GUI thread, which admittedly, takes a
#   negligble amount of time.
#
# Cons:
# - Uses threads when not strictly necessary.
# - Threads must be managed manually.

import sys

import requests
from PySide import QtCore, QtGui

from url import DOWNLOAD_URL
from window import DisplayWidget
from html_parser import parse_html


class DownloadData(QtCore.QThread):
    finished = QtCore.Signal(str)

    def run(self):
        response = requests.get(DOWNLOAD_URL)
        parse_html()
        self.finished.emit(response.text)


class MyWidget(DisplayWidget):
    def __init__(self, parent=None):
        super(MyWidget, self).__init__(parent)

        # We need to store a reference to the thread, otherwise it will be
        # destroyed when the method finishes.
        self._thread = DownloadData()
        self._thread.finished.connect(self._populate_textarea)

    def _button_clicked(self):
        self._thread.start()

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

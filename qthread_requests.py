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

from html_parser import parse_html
from progress import ProgressIndicator


class DownloadData(QtCore.QThread):
    finished = QtCore.Signal(str)

    def run(self):
        response = requests.get(
            'http://www.gutenberg.org/cache/epub/10/pg10.txt')
        parse_html()
        self.finished.emit(response.text)


class MainWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)

        # We need to store a reference to the thread, otherwise it will be
        # destroyed when the method finishes.
        self._thread = DownloadData()
        self._thread.finished.connect(self._populate_textarea)

        self._layout = QtGui.QVBoxLayout(self)
        self._textarea = QtGui.QPlainTextEdit()
        self._textarea.setReadOnly(True)
        self._layout.addWidget(self._textarea)
        self._button = QtGui.QPushButton('Download')
        self._button.clicked.connect(self._button_clicked)
        self._layout.addWidget(self._button)
        self._progress = ProgressIndicator()
        self._layout.addWidget(self._progress)

    def _button_clicked(self):
        self._thread.start()

    def _populate_textarea(self, text):
        self._textarea.setPlainText(text)


def main(argv):
    app = QtGui.QApplication(argv)
    w = MainWidget()
    w.show()
    w.raise_()
    return app.exec_()


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))

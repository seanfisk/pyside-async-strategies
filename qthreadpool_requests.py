#!/usr/bin/env python
#
# Asynchronous using QThreadPool and requests.
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

import requests
from PySide import QtCore, QtGui

from html_parser import parse_html
from progress import ProgressIndicator


class RunnableWithSignals(QtCore.QObject, QtCore.QRunnable):
    def __init__(self, parent=None):
        QtCore.QObject.__init__(self, parent)
        QtCore.QRunnable.__init__(self, parent)


class DownloadData(RunnableWithSignals):
    finished = QtCore.Signal(str)

    def run(self):
        response = requests.get(
            'http://www.gutenberg.org/cache/epub/10/pg10.txt')
        parse_html()
        self.finished.emit(response.text)


class MainWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)

        self._thread_pool = QtCore.QThreadPool.globalInstance()

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
        runnable = DownloadData()
        runnable.finished.connect(self._populate_textarea)
        self._thread_pool.start(runnable)

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

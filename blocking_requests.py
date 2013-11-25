#!/usr/bin/env python
#
# Current synchronous approach.
#
# Pros:
# - Simple.
#
# Cons:
# - Freezes the GUI (which is unacceptable).

import sys

import requests
from PySide import QtGui

from html_parser import parse_html
from progress import ProgressIndicator


class MainWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)

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
        response = requests.get(
            'http://www.gutenberg.org/cache/epub/10/pg10.txt')
        parse_html()
        self._textarea.setPlainText(response.text)


def main(argv):
    app = QtGui.QApplication(argv)
    w = MainWidget()
    w.show()
    w.raise_()
    return app.exec_()


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))

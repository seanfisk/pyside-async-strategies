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

from url import DOWNLOAD_URL
from window import DisplayWidget
from html_parser import parse_html


class MyWidget(DisplayWidget):
    def __init__(self, parent=None):
        super(MyWidget, self).__init__(parent)

    def _button_clicked(self):
        response = requests.get(DOWNLOAD_URL)
        parse_html()
        self._textarea.setPlainText(response.text)


def main(argv):
    app = QtGui.QApplication(argv)
    w = MyWidget()
    w.show()
    w.raise_()
    return app.exec_()


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))

#!/usr/bin/env python
#
# Asynchronous network using QNetworkAccessManager.
#
# Pros:
# - No threads!
# - In my opinion, the solution with the most technical merit (i.e., the "right
#   way to do it").
#
# Cons:
# - Due to the many signals/slots necessary, it does not lend itself to modular
#   and reusable code.
# - Because network code is asynchronous and parsing is not, the current
#   unified HTTP/HTML parsing API would have to be split.
# - Requires significant changes to test code. We cannot use httpretty with
#   requests to test our HTTP requests because QNAM does not utilize Python's
#   socket module.

import sys

from PySide import QtGui, QtNetwork

from html_parser import parse_html
from progress import ProgressIndicator


class MainWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)

        self._qnam = QtNetwork.QNetworkAccessManager()

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
        request = QtNetwork.QNetworkRequest(
            'http://www.gutenberg.org/cache/epub/10/pg10.txt')
        self._reply = self._qnam.get(request)
        self._reply.finished.connect(self._populate_textarea)

    def _populate_textarea(self):
        parse_html()
        self._textarea.setPlainText(unicode(self._reply.readAll(), 'utf-8'))


def main(argv):
    app = QtGui.QApplication(argv)
    w = MainWidget()
    w.show()
    w.raise_()
    return app.exec_()


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))

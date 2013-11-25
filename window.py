from PySide import QtGui


class ProgressIndicator(QtGui.QProgressBar):
    def __init__(self, parent=None):
        super(ProgressIndicator, self).__init__(parent)

        self.setMinimum(0)
        self.setMaximum(0)


class DisplayWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(DisplayWidget, self).__init__(parent)

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
        pass

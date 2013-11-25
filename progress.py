from PySide import QtGui


class ProgressIndicator(QtGui.QProgressBar):
    def __init__(self, parent=None):
        super(ProgressIndicator, self).__init__(parent)

        self.setMinimum(0)
        self.setMaximum(0)

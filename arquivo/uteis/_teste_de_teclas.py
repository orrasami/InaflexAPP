from PySide2 import QtCore, QtGui, QtWidgets

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        QtWidgets.QShortcut(QtGui.QKeySequence("1"), self, activated=self.test_func)
        QtWidgets.QShortcut(QtGui.QKeySequence("2"), self, activated=self.test_func)
        QtWidgets.QShortcut(QtGui.QKeySequence("enter"), self, activated=self.test_func)
        QtWidgets.QShortcut(QtGui.QKeySequence("return"), self, activated=self.test_func)

    @QtCore.Slot()
    def test_func(self):
        shorcut = self.sender()
        sequence = shorcut.key()
        print(sequence.toString())


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
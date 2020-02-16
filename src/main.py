from gui_window import Ui_ShamirSecretSharing
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon
import qdarkstyle


class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_ShamirSecretSharing()
        self.setWindowIcon(QIcon('../res/encryption_30x30.png'))
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        #self.setStyleSheet('QMainWindow{background-color: darkgray;}')
        self.ui.setupUi(self)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = AppWindow()
    w.show()
    sys.exit(app.exec_())

import logging
import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from qfluentwidgets import NavigationItemPosition, FluentWindow
from qfluentwidgets import FluentIcon as FIF

from app.view.home_interface import HomeInterface
from app.view.hostInfo_interface import HostInfoInterface
from app.view.scanner_interface import ScannerInterface


class Window(FluentWindow):
    """ 主界面 """

    def __init__(self):
        super().__init__()

        self.homeInterface = HomeInterface(self)
        self.scannerInterface = ScannerInterface(self)
        self.hostInfoInterface = HostInfoInterface(self)

        self.scannerInterface.updateList.connect(self.hostInfoInterface.update_IpList)

        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FIF.HOME, 'Home')
        self.addSubInterface(self.scannerInterface, FIF.IOT, 'Scanner', NavigationItemPosition.SCROLL)
        self.addSubInterface(self.hostInfoInterface, FIF.VIEW, 'Host Information', parent=self.scannerInterface)

    def initWindow(self):
        self.setFixedSize(900, 700)
        self.setWindowIcon(QIcon(':/qfluentwidgets/images/logo.png'))
        self.setWindowTitle('Miku Scanner')


if __name__ == '__main__':
    logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec()

# coding:utf-8
from PySide6.QtCore import Signal
from PySide6.QtGui import QPixmap, QFont, Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from qfluentwidgets import LineEdit, ComboBox, SpinBox, PushButton, FluentIcon, ProgressRing, \
    InfoBar, InfoBarIcon, InfoBarPosition

from app.network.PingScan import PingScan
from app.network.TcpAckScan import TcpAckScan
from app.network.TcpConnectScan import TcpConnectScan
from app.network.TcpSynScan import TcpSynScan

style = """
#title {
    font: 42px 'Segoe UI SemiBold', 'Microsoft YaHei SemiBold';
    background-color: transparent;
    color: black;
}
#low_title {
    font: 15px 'Segoe UI SemiBold', 'Microsoft YaHei SemiBold';
    background-color: transparent;
    color: black;
}
#scanFont {
    font: 25px 'Segoe UI SemiBold', 'Microsoft YaHei SemiBold';
    background-color: transparent;
    color: black;
}
"""



class ScannerInterface(QWidget):
    updateList = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setObjectName('ScannerInterface')
        self.vBoxLayout = QVBoxLayout()
        self.setStyleSheet(style)
        view = QWidget(self)
        view.resize(850, 650)

        # 标题
        title = QLabel('Discover hosts', view)
        title.setObjectName("title")
        title.move(40, 35)
        low_title = QLabel('Step 1: Enter the IP or IP segment to be scanned and specify the port to start scanning.', view)
        low_title.setObjectName("low_title")
        low_title.move(40, 89)

        # IP
        ip_label = QLabel('IP', view)
        ip_label.setObjectName("scanFont")
        ip_label.move(34, 150)
        self.ip_input = LineEdit(view)
        self.ip_input.setFixedWidth(279)
        self.ip_input.setMinimumHeight(47)
        self.ip_input.setClearButtonEnabled(True)
        self.ip_input.move(34, 187)

        # Port
        port_label = QLabel('Port', view)
        port_label.setObjectName("scanFont")
        port_label.move(357, 150)
        self.port_input = LineEdit(view)
        self.port_input.setFixedWidth(117)
        self.port_input.setMinimumHeight(47)
        self.port_input.setClearButtonEnabled(True)
        self.port_input.move(357, 187)

        # Mode
        mode_label = QLabel('Mode', view)
        mode_label.setObjectName("scanFont")
        mode_label.move(34, 273)
        self.mode_input = ComboBox(view)
        self.mode_input.addItems(
            ['TCP Connect Scanning', 'TCP SYN Scanning', 'TCP ACK Scanning', 'Ping Scanning']
        )
        mode_font = QFont()
        mode_font.setPointSize(12)
        self.mode_input.setFont(mode_font)
        self.mode_input.setCurrentIndex(0)
        self.mode_input.setMinimumSize(210, 47)
        self.mode_input.move(34, 310)
        # 当进行选择时进行界面差异变化
        self.mode_input.currentIndexChanged.connect(self.modeChange)

        # Number of threads
        threads_label = QLabel('Number of threads', view)
        threads_label.setObjectName("scanFont")
        threads_label.move(313, 273)
        self.threads_input = SpinBox(view)
        self.threads_input.setMaximum(10000)
        self.threads_input.setMinimumHeight(47)
        self.threads_input.move(313, 310)

        # 开始和停止按钮
        self.start_button = PushButton('Start Scanning', view, FluentIcon.SYNC)
        self.start_button.setMinimumHeight(47)
        self.start_button.move(80, 413)
        self.start_button.clicked.connect(self.Scanning)
        self.stop_button = PushButton('Stop Scanning', view, FluentIcon.CLOSE)
        self.stop_button.setEnabled(False)
        self.stop_button.setMinimumHeight(47)
        self.stop_button.move(274, 413)
        self.stop_button.clicked.connect(self.scan_stop)

        # 状态显示
        state_label = QLabel('State', view)
        state_label.setObjectName('scanFont')
        state_label.move(595, 150)
        self.state_ring = ProgressRing(view)
        self.state_ring.setFixedSize(142, 142)
        self.state_ring.setTextVisible(True)
        self.state_ring.move(636, 211)

        # tip
        content = "The first scanning method is not recommended, it is very slow!\nYou can try other scanning methods.More scanning methods \nmay be added in the future and the scanning speed may be \noptimized."
        infoBar = InfoBar(
            icon=InfoBarIcon.INFORMATION,
            title='Tip',
            content=content,
            orient=Qt.Vertical,
            isClosable=False,
            duration=-1,
            position=InfoBarPosition.NONE,
            parent=view
        )
        infoBar.move(20, 492)

        # 背景图片
        backImage = QLabel(view)
        backImage.setPixmap(QPixmap('./app/resource/images/header-scanner.png'))
        backImage.resize(366, 650)
        backImage.setScaledContents(True)
        backImage.move(484, 0)

        # 扫描任务以及相关变量
        self.scan_work = None
        self.ip_list = []

    # UI界面变化-在选择不同模式下各控件状态
    def modeChange(self):
        match self.mode_input.currentIndex():
            case 0:
                self.ip_input.setEnabled(True)
                self.port_input.setEnabled(True)
                self.threads_input.setEnabled(True)
            case 1:
                self.port_input.setEnabled(False)
                self.threads_input.setEnabled(False)
            case 2:
                self.port_input.setEnabled(False)
                self.threads_input.setEnabled(False)
            case 3:
                self.port_input.setEnabled(False)
                self.threads_input.setEnabled(False)


    # 开始扫描任务逻辑实现
    def scan_stop(self):
        InfoBar.info(
            title='Scan Stopping',
            content='Please wait patiently for the result.',
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=4000,
            parent=self
        )
        self.stop_button.setEnabled(False)
        self.scan_work.requestInterruption()

    def scan_stop_siganl(self):
        self.scan_work = None
        self.start_button.setEnabled(True)
        InfoBar.success(
            title='Scan Stopped',
            content='The scan has stopped.',
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=4000,
            parent=self
        )


    def scan_end(self):
        InfoBar.success(
            title='Scan End',
            content=f'A total of {len(self.ip_list)} hosts were found to be alive.',
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=4000,
            parent=self
        )
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.scan_work.deleteLater()
        self.scan_work = None

    def updateList_func(self, new_ipList):
        self.ip_list = new_ipList
        self.updateList.emit(self.ip_list)


    def Scanning(self):
        self.state_ring.setValue(0)
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        InfoBar.info(
            title='Scanning',
            content='Please wait patiently for the result.',
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=4000,
            parent=self
        )
        match self.mode_input.currentIndex():
            case 0:
                self.scan_work = TcpConnectScan(
                    int(self.threads_input.text()),
                    self.ip_input.text(),
                    self.port_input.text(),
                    self.state_ring
                )
            case 1:
                self.scan_work = TcpSynScan(
                    self.ip_input.text(),
                    self.state_ring
                )
            case 2:
                self.scan_work = TcpAckScan(
                    self.ip_input.text(),
                    self.state_ring
                )

            case 3:
                self.scan_work = PingScan(
                    self.ip_input.text(),
                    self.state_ring
                )

        self.scan_work.stopSignal.connect(self.scan_stop_siganl)
        self.scan_work.endReady.connect(self.scan_end)
        self.scan_work.updateList.connect(self.updateList_func)
        self.scan_work.start()




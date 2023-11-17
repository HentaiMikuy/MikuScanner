# coding:utf-8
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, QHBoxLayout, QLabel
from qfluentwidgets import TabBar, TabCloseButtonDisplayMode, qrouter, FluentIcon

from app.components.table_frame import TableFrame

style = """
PivotInterface QLabel,
TabInterface QLabel {
    padding-left: 10px;
    font: 14px 'Segoe UI', 'Microsoft YaHei', 'PingFang SC';
    color: black;
}

#controlPanel BodyLabel {
    padding-left: 0px;
}

#controlPanel {
    background-color: white;
    border-left: 1px solid rgb(229, 229, 229);
    border-top-right-radius: 10px;
}
#tabView {
    border-top: 2px solid rgb(229, 229, 229);
    border-left: 2px solid rgb(229, 229, 229);
    border-radius: 10px;
}
#exampleInterface {
    font-size: 20px;
    font-weight: bold;
}
"""

tabFont_style = """
#font_1 {
    font-size: 20px;
    font-weight: bold;
}
#font_2 {
    font-size: 12px;
}
"""

class newHostInfoTab(QWidget):

    def __init__(self, osInfo: str, portInfos,parent=None):
        super().__init__(parent=parent)
        self.setStyleSheet(tabFont_style)
        self.osInfo = osInfo
        self.portInfos = portInfos
        self.vBoxLayout = QVBoxLayout()
        view = QWidget(self)
        view.resize(522, 224)

        # OS Information
        os_label = QLabel('OS:', view)
        os_label.setObjectName("font_1")
        os_label.move(15, 8)
        os_content = QLabel(self.osInfo, view)
        os_content.setFixedWidth(445)
        os_content.setWordWrap(True)
        os_content.setObjectName("font_2")
        os_content.move(30, 40)

        # Port Information
        port_table = TableFrame(self.portInfos, view)
        port_table.move(40, 90)


class TabInterface(QWidget):
    """ Tab interface """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.tabCount = 1

        self.tabBar = TabBar(self)
        self.tabBar.setFixedWidth(600)
        self.stackedWidget = QStackedWidget(self)
        self.tabView = QWidget(self)
        self.tabView.setObjectName('tabView')

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout(self.tabView)

        example_text = "💕\nOnce you've selected your IP, \nclick the button to get the details of the target host!👍\n💕"
        self.exampleInterface = QLabel(example_text, self)
        self.exampleInterface.setAlignment(Qt.AlignCenter)

        # add items to pivot
        self.__initWidget()

    def __initWidget(self):
        self.initLayout()
        self.setStyleSheet(style)
        # 设置标签页移动 阴影
        self.tabBar.setCloseButtonDisplayMode(TabCloseButtonDisplayMode.ON_HOVER)
        self.tabBar.setMovable(True)
        self.tabBar.setTabShadowEnabled(True)

        self.addSubInterface(self.exampleInterface,
                             'exampleInterface', 'Example', FluentIcon.GLOBE)

        self.connectSignalToSlot()

        qrouter.setDefaultRouteKey(
            self.stackedWidget, self.exampleInterface.objectName())

    def connectSignalToSlot(self):
        # self.tabBar.tabAddRequested.connect(self.addTab)
        self.tabBar.tabCloseRequested.connect(self.removeTab)


    def initLayout(self):
        self.tabBar.setTabMaximumWidth(200)

        self.setFixedHeight(280)
        self.hBoxLayout.addWidget(self.tabView, 1)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)

        self.vBoxLayout.addWidget(self.tabBar)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)

    def addSubInterface(self, widget, objectName, text, icon):
        widget.setObjectName(objectName)
        # widget.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.stackedWidget.addWidget(widget)
        self.tabBar.addTab(
            routeKey=objectName,
            text=text,
            icon=icon,
            onClick=lambda: self.stackedWidget.setCurrentWidget(widget)
        )

    def addTab(self, host, OsInfo, PortInfos):
        self.addSubInterface(newHostInfoTab(OsInfo, PortInfos), host, host, FluentIcon.GLOBE)

    def removeTab(self, index):
        item = self.tabBar.tabItem(index)
        widget = self.findChild(QLabel, item.routeKey())

        self.stackedWidget.removeWidget(widget)
        self.tabBar.removeTab(index)
        widget.deleteLater()
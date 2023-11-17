# coding:utf-8
from PySide6.QtGui import QPixmap, Qt
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from qfluentwidgets import FluentIcon

from app.components.link_card import LinkCardView
from app.components.type_writer import TypewriterLabel


class HomeInterface(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setObjectName('HomeInterface')
        self.vBoxLayout = QVBoxLayout()

        self.view = QWidget(self)
        self.view.resize(850, 650)
        # 主页背景
        banner = QLabel(self.view)
        banner.setPixmap(QPixmap('./app/resource/images/header.png'))
        banner.resize(850, 478)
        banner.move(0, 172)
        banner.lower()
        banner.setScaledContents(True)
        # 主页logo
        logo = QLabel(self.view)
        logo.setPixmap(QPixmap('./app/resource/images/logo.png'))
        logo.resize(534, 130)
        logo.move(50, 42)
        logo.setScaledContents(True)
        # 主页介绍 - 动态打字效果
        introduction = TypewriterLabel(self.view)
        introduction.resize(550, 115)
        introduction.move(50, 200)
        # Card
        moreView = LinkCardView(self.view)
        moreView.addCard(
            ':/qfluentwidgets/images/logo.png',
            'Power by \nQFluentWidgets',
            'Rapidly build modern GUI without ever writing any style sheet.',
            "https://qfluentwidgets.com/"
        )
        moreView.addCard(
            FluentIcon.GITHUB,
            'Github repo',
            'The latest fluent design controls and styles for your applications.',
            ""
        )
        moreView.addCard(
            FluentIcon.CODE,
            'Code samples',
            'Find samples that demonstrate specific tasks, features and APIs.',
            ""
        )
        moreView.addCard(
            FluentIcon.FEEDBACK,
            'Send feedback',
            'Help us improve MikuScanner by providing feedback.',
            ""
        )
        moreView.move(0, 360)



        self.vBoxLayout.addWidget(self.view, 1, Qt.AlignCenter)


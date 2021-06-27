from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout

import ibs

g_api: Optional[ibs.API] = None


class MainWidget(QWidget):
    def __init__(self):
        super(MainWidget, self).__init__(flags=Qt.WindowFlags())

        layout = QHBoxLayout()
        layout.addWidget(QLabel("test 1"))
        self.setLayout(layout)


def startup(api, widget):
    global g_api
    g_api = api
    g_api.log.info("Test1 extension startup")


def shutdown():
    g_api.log.info("Test1 extension shutdown")

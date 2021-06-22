import logging

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout

g_api = None


class MainWidget(QWidget):
    def __init__(self):
        super(MainWidget, self).__init__(flags=Qt.WindowFlags())

        layout = QHBoxLayout()
        layout.addWidget(QLabel("test 1"))
        self.setLayout(layout)


def startup(api):
    global g_api
    g_api = api
    logging.info("Test1 extension startup")


def shutdown():
    logging.info("Test1 extension shutdown")

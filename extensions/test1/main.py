import logging

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget

api = None


class Widget(QWidget):
    def __init__(self):
        super(Widget, self).__init__(flags=Qt.WindowFlags())


def startup():
    logging.info("Test1 component startup")


def shutdown():
    logging.info("Test1 component shutdown")

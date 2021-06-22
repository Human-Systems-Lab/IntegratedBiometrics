from typing import Tuple

from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout

import ibs
from ibs import LayoutHint
from . import main


class Extension(ibs.IbsExt):
    def __init__(self, options):
        pass

    @staticmethod
    def get_name() -> str:
        return "test 1"

    def startup_ref(self):
        pass

    def shutdown_ref(self):
        pass

    def get_widget(self) -> QWidget:
        pass


class Options(ibs.IbsOpt):
    def __init__(self):
        super(Options, self).__init__()

        layout = QVBoxLayout()
        layout.addWidget(QLabel("test options"))
        self.setLayout(layout)

    def get_config(self):
        return None

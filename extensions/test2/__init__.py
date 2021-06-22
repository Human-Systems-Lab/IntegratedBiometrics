from typing import Tuple

from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout

import ibs
from ibs import LayoutHint


class Extension(ibs.IbsExt):
    def __init__(self, options):
        pass

    @staticmethod
    def get_name() -> str:
        return "test 2"

    def startup_ref(self):
        pass

    def shutdown_ref(self):
        pass

    def get_widget(self) -> QWidget:
        pass

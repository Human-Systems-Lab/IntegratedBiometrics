from typing import Tuple, Optional

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
        return lambda api, widget: api.log.info("Startup test 2")

    def shutdown_ref(self):
        return lambda: print("Shutdown test 2")

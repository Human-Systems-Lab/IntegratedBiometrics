from typing import Optional

from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout

import ibs
from ibs import LayoutHint
from . import main


class Extension(ibs.IbsExt):
    def __init__(self, options):
        super(Extension, self).__init__(options)

    @staticmethod
    def get_name() -> str:
        return "test 1"

    def startup_ref(self):
        return main.startup

    def shutdown_ref(self):
        return main.shutdown

    def get_guicfg(self) -> Optional[ibs.IbsGuiCfg]:
        class GuiCfg(ibs.IbsGuiCfg):
            def get_widget(self) -> QWidget:
                return main.MainWidget()

            def get_layout(self) -> LayoutHint:
                return LayoutHint.Top

        return GuiCfg()


class Options(ibs.IbsOpt):
    # noinspection PyArgumentList
    def __init__(self):
        super(Options, self).__init__()

        layout = QVBoxLayout()
        layout.addWidget(QLabel("test options"))
        self.setLayout(layout)

    def get_config(self):
        return None

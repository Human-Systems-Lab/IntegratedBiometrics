from typing import Optional

from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout

import ibs
from ibs import LayoutHint
from . import main


class Extension(ibs.IbsExt):
    def __init__(self, options):
        super(Extension, self).__init__(options)

        self.use_gui = options["use_gui"]

    @staticmethod
    def get_name() -> str:
        return "Blink Detection"

    def startup_ref(self):
        return main.startup

    def shutdown_ref(self):
        return main.shutdown

    def get_guicfg(self) -> Optional[ibs.IbsGuiCfg]:
        class GuiCfg(ibs.IbsGuiCfg):
            def get_widget(self) -> QWidget:
                return main.BlinkDetector()

            def get_layout(self) -> LayoutHint:
                return LayoutHint.Center

        if self.use_gui:
            return GuiCfg()
        else:
            return None


class Options(ibs.IbsOpt):
    # noinspection PyArgumentList
    def __init__(self):
        super(Options, self).__init__()

        self.dsp_button = QCheckBox("Show Videofeed")

        layout = QVBoxLayout()
        layout.addWidget(self.dsp_button)
        self.setLayout(layout)

    def get_config(self):
        return {
            "use_gui": self.dsp_button.isChecked()
        }

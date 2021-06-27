import logging
from abc import ABC
from threading import Lock
from typing import Callable, Tuple, Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget

import impl
import config


class API:
    def __init__(self, ext: str):
        self.extname = ext
        self.log = logging

    @staticmethod
    def read_frame():
        """
        Retrieves a frame from the webcam; Ensures compatibility with other extensions

        Returns:
            Numpy array with raw frame data: [height, width, 3]; 0 < ret[:,:,:] < 255
        """
        return impl.fmang.read_frame()

    def send_data(self, data: bytes):
        pass


class LayoutHint(int):
    Center = 0
    Left = 1
    LeftFull = 2
    LeftTop = 3
    LeftBottom = 4
    LeftFloat = 5
    LeftCenter = 6
    Top = 7
    TopFull = 8
    TopLeft = 9
    TopRight = 10
    TopFloat = 11
    TopCenter = 12
    Right = 13
    RightFull = 14
    RightTop = 15
    RightBottom = 16
    RightFloat = 17
    RightCenter = 18
    Bottom = 19
    BottomFull = 20
    BottomLeft = 21
    BottomRight = 22
    BottomFloat = 23
    BottomCenter = 24


class IbsGuiCfg:
    """
    Abstract gui component interface
    """
    def get_widget(self) -> QWidget:
        raise NotImplementedError()

    def get_layout(self) -> LayoutHint:
        raise NotImplementedError()


class IbsExt:
    """
    Abstract component interface
    """
    def __init__(self, options):
        self.options = options

    @staticmethod
    def get_name() -> str:
        raise NotImplementedError()

    def startup_ref(self) -> Callable[[API, QWidget], None]:
        raise NotImplementedError()

    def shutdown_ref(self) -> Callable[[], None]:
        raise NotImplementedError()

    # noinspection PyMethodMayBeStatic
    def get_guicfg(self) -> Optional[IbsGuiCfg]:
        return None


class IbsOpt(QWidget):
    """
    Abstract options inferface
    """
    def __init__(self):
        super().__init__(flags=Qt.WindowFlags())

    def get_config(self):
        raise NotImplementedError()

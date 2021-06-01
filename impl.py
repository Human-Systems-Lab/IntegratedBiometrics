import logging
from threading import Thread, Lock
from typing import Optional

import cv2
import numpy as np


class _FrameManager:  # Singleton
    def __init__(self):
        self._cap = cv2.VideoCapture(0)
        th = Thread(target=self._read_webcam, daemon=True)

        self._lock = Lock()
        th.start()

    def read_frame(self):
        with self._lock:
            return np.copy(self.frame)

    def _read_webcam(self):
        # Immediately grab the lock before anyone else can
        with self._lock:
            ret, frame = self._cap.read()
            if not ret:
                exit(1)  # Probably not the best way of dealing with this
            self.frame = frame

        while True:
            ret, frame = self._cap.read()
            if not ret:
                continue
            with self._lock:
                self.frame = frame


fmang: Optional[_FrameManager] = None


def start():
    global fmang
    fmang = _FrameManager()
    logging.basicConfig(level=logging.INFO)

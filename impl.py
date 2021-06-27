import time
import logging
from threading import Thread, Lock
from typing import Optional

import cv2
import numpy as np


#
# This file contains the logic for accessing shared resourses across extensions
#


class _FrameManager:  # Singleton
    def __init__(self):
        self._cap_lock = Lock()
        with self._cap_lock:
            self._cap = cv2.VideoCapture(0)
            if not self._cap:
                raise RuntimeError("Unable to retrieve a webcam")
            ret, frame = self._cap.read()
        if not ret:
            raise RuntimeError("Unable to access the video camera")
        self.frame = frame
        th = Thread(target=self._read_webcam, daemon=True)

        self._lock = Lock()
        th.start()

    def read_frame(self):
        with self._lock:
            return self.frame.copy()

    def _read_webcam(self):
        while True:
            with self._cap_lock:
                if self._cap.isOpened():
                    ret, frame = self._cap.read()
                else:
                    raise RuntimeError("Webcam closed unexpectedly")
            if not ret:
                logging.warning("Failed to retrieve frame from video feed")
                time.sleep(1)
                continue
            with self._lock:
                frame = np.resize(frame, self.frame.shape)
                self.frame[...] = frame[...]


fmang: Optional[_FrameManager] = None


def start():
    global fmang
    fmang = _FrameManager()
    logging.basicConfig(level=logging.INFO)

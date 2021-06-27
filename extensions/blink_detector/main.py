import time
import math

import cv2
import imutils
import numpy as np
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QPolygonF
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout

import ibs
from .detector import Model, measure

running = True


class TimeGraph(QWidget):
    # noinspection PyArgumentList
    def __init__(self, retention=30.0, ymin=0.0, ymax=1.0, back_color="white", data_color="red"):
        super(TimeGraph, self).__init__()

        self.setMinimumWidth(320)
        self.setMinimumHeight(80)

        self.yscale = 1 / (ymax - ymin)
        self.xscale = 1 / retention
        self.yoffset = ymin

        self.retention = retention
        self.data = list()

        self.data_pen = QtGui.QPen()
        self.data_pen.setColor(QtGui.QColor(data_color))
        self.data_pen.setWidth(3)
        self.data_pen.setStyle(Qt.SolidLine)
        self.data_pen.setCapStyle(Qt.RoundCap)
        self.data_pen.setJoinStyle(Qt.RoundJoin)

        self.back_brush = QtGui.QBrush()
        self.back_brush.setColor(QtGui.QColor(back_color))
        self.back_brush.setStyle(Qt.SolidPattern)

    def add_point(self, p):
        self.data.append((time.time(), p))

    def paintEvent(self, event):
        # This is not efficient, but without using C idk how to make it better
        t = time.time()
        while len(self.data) != 0 and t - self.data[0][0] > self.retention:
            del self.data[0]

        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        dev = painter.device()
        width = dev.width()
        height = dev.height()

        painter.setBrush(self.back_brush)
        painter.drawRect(0, 0, width, height)

        painter.setPen(self.data_pen)
        data_points = [
            QPoint(
                int(width * (self.xscale * (x - t) + 1)),
                int(height * (1 - self.yscale * (y - self.yoffset)))
            ) for x, y in self.data
        ]
        painter.drawPolyline(QPolygonF(data_points))

        painter.end()
        self.update()


class ImgDsp(QLabel):
    def __init__(self):
        super(ImgDsp, self).__init__()

        self.setMinimumWidth(640)
        self.setMinimumHeight(480)
        self.setAlignment(Qt.AlignCenter)

    def show_img(self, frame: np.ndarray, kpts):
        frame = frame[..., ::-1].astype(np.uint8)
        if kpts is not None:
            for x, y in kpts:
                cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)

        h, w, ch = frame.shape
        bpl = ch * w
        qt_fmt = QImage(frame.data, w, h, bpl, QImage.Format_RGB888)

        sz = self.size()
        p = qt_fmt.scaled(sz.width(), sz.height(), Qt.KeepAspectRatio)

        # noinspection PyArgumentList
        self.setPixmap(QPixmap.fromImage(p))


class BlinkDetector(QWidget):
    # noinspection PyArgumentList
    def __init__(self):
        super(BlinkDetector, self).__init__()

        self.webcam = ImgDsp()
        self.lgraph = TimeGraph(ymin=0.1, ymax=0.4)
        self.rgraph = TimeGraph(ymin=0.1, ymax=0.4)

        glayout = QHBoxLayout()
        glayout.addWidget(self.lgraph)
        glayout.addWidget(self.rgraph)
        gwidget = QWidget()
        gwidget.setLayout(glayout)

        layout = QVBoxLayout()
        layout.addWidget(self.webcam)
        layout.addWidget(gwidget)
        self.setLayout(layout)


def startup(api, widget: BlinkDetector):
    mdl = Model()

    if widget:
        while running:
            frame: np.ndarray = api.read_frame()
            frame = imutils.resize(frame, width=500)
            kpts_set = mdl.forward(frame)
            kpts = None
            if len(kpts_set) > 0:
                kpts = kpts_set[0]
                lval, rval = measure(kpts)
                widget.lgraph.add_point(lval)
                widget.rgraph.add_point(rval)
            widget.webcam.show_img(frame, kpts)
    else:
        raise NotImplementedError("Blink detection without showing video is not implemented")


def shutdown():
    global running
    running = False

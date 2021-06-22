import os
import sys
import importlib
from threading import Thread
from typing import Optional, Type, Dict, List

from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout

import ibs
import impl
import config


class MainWindow(QWidget):
    def __init__(self, exts: List[ibs.IbsExt]):
        super(MainWindow, self).__init__(flags=Qt.WindowFlags())

        self.exts = exts
        self.ext_ths = list()
        for e in self.exts:
            # TODO: create and add an API obj arg to each of the threads
            th = Thread(target=e.startup_ref())
            th.start()
            self.ext_ths.append(th)

    def shutdown(self):
        # Application shutdown
        for e in self.exts:
            e.shutdown_ref()()  # Calling from the main thread
        for th in self.ext_ths:
            th.join()


def invalid_extensions(app):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText("Unable to find any extensions")
    msg.setWindowTitle("Error")
    msg.setStandardButtons(QMessageBox.Ok)
    msg.show()
    app.exec_()
    sys.exit(1)


class ExpandButton(QWidget):
    def __init__(self, callback, xsize=15, ysize=15, squish=1.75):  # 1 < squish < 2.5
        super(ExpandButton, self).__init__(flags=Qt.WindowFlags())

        self.sz = QtCore.QSize(xsize, ysize)
        self.pressed = False
        self.callback = callback
        self.resize(xsize, ysize)

        xpad = xsize // 5
        ypad = ysize // 5
        up_point_list = list()
        up_point_list.append(QtCore.QPoint(int(squish * xpad), ypad))
        up_point_list.append(QtCore.QPoint(xsize - int(squish * xpad), ysize // 2))
        up_point_list.append(QtCore.QPoint(int(squish * xpad), ysize - ypad))
        self.up_poly = QtGui.QPolygonF(up_point_list)
        down_point_list = list()
        down_point_list.append(QtCore.QPoint(xpad, int(squish * ypad)))
        down_point_list.append(QtCore.QPoint(xsize // 2, ysize - int(squish * ypad)))
        down_point_list.append(QtCore.QPoint(xsize - xpad, int(squish * ypad)))
        self.down_poly = QtGui.QPolygonF(down_point_list)

        self.pen = QtGui.QPen()
        self.pen.setColor(QtGui.QColor("black"))
        self.pen.setWidth(xsize // 10)
        self.pen.setStyle(Qt.SolidLine)
        self.pen.setCapStyle(Qt.RoundCap)
        self.pen.setJoinStyle(Qt.RoundJoin)

        self.update()

    def sizeHint(self):
        return self.sz

    def paintEvent(self, e):
        if self.isEnabled():
            painter = QtGui.QPainter()
            painter.begin(self)
            painter.setRenderHint(QtGui.QPainter.Antialiasing)
            painter.setPen(self.pen)

            if self.pressed:
                painter.drawPolyline(self.down_poly)
            else:
                painter.drawPolyline(self.up_poly)
            painter.end()

    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.pressed = not self.pressed
            self.update()
            self.callback()
        else:
            super().mousePressEvent(event)


class ToggleExpandable(QWidget):
    # noinspection PyArgumentList
    def __init__(self, name: str, widget: Optional[QWidget]):
        super(ToggleExpandable, self).__init__(flags=Qt.WindowFlags())

        self.expand_button = ExpandButton(self.on_expand)
        if widget is None:
            self.expand_button.setEnabled(False)
        self.check_box = QCheckBox()
        self.label = QLabel(name)
        self.widget = widget
        if widget is not None:
            self.widget.setEnabled(False)

        base_layout = QHBoxLayout()
        base_layout.addWidget(self.expand_button)
        base_layout.addWidget(self.check_box)
        base_layout.addWidget(self.label)
        if widget is None:
            self.setLayout(base_layout)
        else:
            self.base_widget = QWidget()
            self.base_widget.setLayout(base_layout)

            self.layout = QVBoxLayout()
            self.layout.setSpacing(0)
            self.layout.setContentsMargins(0, 0, 0, 0)
            self.layout.addWidget(self.base_widget)
            self.setLayout(self.layout)

            self.check_box.pressed.connect(lambda: self.widget.setEnabled(not self.check_box.isChecked()))

    # noinspection PyArgumentList
    def on_expand(self):
        if self.expand_button.pressed:
            self.layout.addWidget(self.widget)
        else:
            self.layout.removeWidget(self.widget)
            self.widget.setParent(None)


class StartupWindow(QWidget):
    # noinspection PyArgumentList, PyUnresolvedReferences
    def __init__(self, extmap: Dict[Type[ibs.IbsExt], Optional[Type[ibs.IbsOpt]]], exts: List[ibs.IbsExt]):
        super(StartupWindow, self).__init__(flags=Qt.WindowFlags())
        self.continued = False

        self.exts = exts
        self.extmap: Dict[Type[ibs.IbsExt], Optional[ibs.IbsOpt]] = dict()
        te_layout = QVBoxLayout()
        for ext in extmap:
            name = ext.get_name()
            if extmap[ext]:
                self.extmap[ext] = extmap[ext]()
            else:
                self.extmap[ext] = None
            extopt = ToggleExpandable(name, self.extmap[ext])
            te_layout.addWidget(extopt)
        te_layout.setAlignment(QtCore.Qt.AlignTop)
        te_widget = QWidget()
        te_widget.setLayout(te_layout)

        continue_button = QPushButton("Continue")
        continue_button.pressed.connect(self.on_continue)
        layout = QVBoxLayout()
        layout.addWidget(te_widget)
        layout.addWidget(continue_button)
        self.setLayout(layout)

    def on_continue(self):
        for ext in self.extmap:
            self.exts.append(ext(self.extmap[ext]))
        self.continued = True
        self.close()

    def closeEvent(self, event):
        if self.continued:
            super().closeEvent(event)
        else:
            sys.exit(0)


def main():
    impl.start()
    app = QApplication(sys.argv)

    # Loading extensions
    if not os.path.isdir("extensions") or not os.path.isfile("extensions/__init__.py"):
        invalid_extensions(app)

    exts = os.listdir("extensions")
    exts = [e for e in exts if e != "__init__.py"]
    if len(exts) == 0:
        invalid_extensions(app)

    extmap = dict()
    for e in exts:
        if e.endswith(".py"):
            e = e[:-3]
        config.current_ext = e
        module = importlib.import_module("extensions.%s" % e)
        if not hasattr(module, "Extension"):
            continue
        if hasattr(module, "Options"):
            extmap[module.Extension] = module.Options
            continue
        extmap[module.Extension] = None

    # Configuring extensions
    exts = list()  # This will get initialized by the startup window
    window = StartupWindow(extmap, exts)
    window.show()
    e_code = app.exec_()
    if e_code != 0:
        sys.exit(e_code)

    # Launching extensions
    window = MainWindow(exts)
    window.show()
    e_code = app.exec_()
    window.shutdown()
    sys.exit(e_code)


if __name__ == "__main__":
    main()
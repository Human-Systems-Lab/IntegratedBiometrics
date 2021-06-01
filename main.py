import os
import sys
import importlib
from threading import Thread

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QWidget

import impl
import config


class MainWindow(QWidget):
    def __init__(self, flags=None):
        super(MainWindow, self).__init__(flags=flags)
        pass


def invalid_extensions(app):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText("Unable to find any extensions")
    msg.setWindowTitle("Error")
    msg.setStandardButtons(QMessageBox.Ok)
    msg.show()
    app.exec_()
    sys.exit(1)


def main():
    impl.start()
    app = QApplication(sys.argv)

    if not os.path.isdir("extensions") or not os.path.isfile("extensions/__init__.py"):
        invalid_extensions(app)

    exts = os.listdir("extensions")
    exts = [e for e in exts if e != "__init__.py"]
    if len(exts) == 0:
        invalid_extensions(app)

    for e in exts:
        config.current_name = e
        importlib.import_module("extensions.%s" % e)

    cmp_ths = list()
    for e in config.components:
        th = Thread(target=e.startup_ref())
        th.start()
        cmp_ths.append(th)

    window = MainWindow(flags=Qt.WindowFlags())
    window.show()
    e_code = app.exec_()

    # Application shutdown
    for e in config.components:
        e.shutdown_ref()()  # Calling from the main thread
    for th in cmp_ths:
        th.join()
    sys.exit(e_code)


if __name__ == "__main__":
    main()

# File: MayaUtils.py

from PySide2.QtWidgets import QWidget
import shiboken2
import maya.OpenMayaUI as omui
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QDialog

from PySide2.QtWidgets import QMainWindow
from PySide2.QtGui import QWindow
from PySide2.QtWidgets import QVBoxLayout
from PySide2.QtWidgets import QPushButton

from PySide2.QtWidgets import QDialog
from PySide2.QtWidgets import QLayout
from PySide2.QtWidgets import QWidget
from PySide2.QtWidgets import QVBoxLayout

from PySide2.QtWidgets import QWidget, QMainWindow
from PySide2.QtCore import Qt


def get_maya_main_window():
    from maya.OpenMayaUI import MQtUtil
    from shiboken2 import wrapInstance
    main_window_ptr = MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QWidget)


class QMayaWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent or get_maya_main_window(), Qt.Window)


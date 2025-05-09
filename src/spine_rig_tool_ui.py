import maya.cmds as mc
from PySide2.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSlider, QWidget, QMessageBox
)
from PySide2.QtCore import Qt

from MayaUtils import QMayaWindow
from ColorPicker import ColorPicker
from spine_rigger import SpineRigger


class SpineRigToolWidget(QMayaWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Spine Rigging Tool")

        self.controller_size = 5

        self.masterLayout = QVBoxLayout()
        self.setLayout(self.masterLayout)

        self.tipLabel = QLabel("please pcik spine joints (in order!) before clicking 'Rig Spine'")
        self.masterLayout.addWidget(self.tipLabel)

        # Controller size slider
        sliderLayout = QHBoxLayout()
        self.ctrlSizeSlider = QSlider(Qt.Horizontal)
        self.ctrlSizeSlider.setRange(1, 30)
        self.ctrlSizeSlider.setValue(self.controller_size)
        self.ctrlSizeSlider.valueChanged.connect(self.ctrlSizeChanged)
        self.ctrlSizeLabel = QLabel(f"{self.controller_size}")
        sliderLayout.addWidget(QLabel("Controller Size"))
        sliderLayout.addWidget(self.ctrlSizeSlider)
        sliderLayout.addWidget(self.ctrlSizeLabel)
        self.masterLayout.addLayout(sliderLayout)

        # Color picker
        self.colorPicker = ColorPicker()
        self.masterLayout.addWidget(self.colorPicker)

        # Rig button
        self.rigBtn = QPushButton("Rig Spine")
        self.rigBtn.clicked.connect(self.rigSpine)
        self.masterLayout.addWidget(self.rigBtn)

    def ctrlSizeChanged(self, value):
        self.controller_size = value
        self.ctrlSizeLabel.setText(f"{value}")

    def rigSpine(self):
        selected_joints = mc.ls(sl=True, type="joint")
        if len(selected_joints) < 3:
            QMessageBox.critical(self, "Error", "Please select at least 3 joints in order!")
            return

        color = self.colorPicker.getColor()
        r, g, b = color.redF(), color.greenF(), color.blueF()

        rigger = SpineRigger(
            spine_joints=selected_joints,
            controller_size=self.controller_size,
            color=(r, g, b)
        )
        rigger.rig()


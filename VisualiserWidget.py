from PyQt5.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
    QCheckBox,
    QButtonGroup
)
from PyQt5.QtGui import QColor
from PitchWidget import PitchWidget
import json

class VisualiserWidget(QWidget):
    """A widget containing the pitch and visualiser options."""
    
    def __init__(self, config,parent = None):
        """Constructs a VisualiserWidget using configurations.

        Args:
            config (dict): a dictionary of configurations
            parent (PyQt5.QWidgets.QWidget, optional): Parent widget. 
            Defaults to None.
        """
        super().__init__(parent=parent)

        self.setGeometry(0,0,500,500)
        vLayout = QVBoxLayout(self)
        hLayout = QHBoxLayout()

        # create options pane
        self.modeButtons = QButtonGroup()
        passes = QCheckBox("Passes")
        shots = QCheckBox("Shots")
        heatmap = QCheckBox("Heatmap")
        self.modeButtons.addButton(passes, id=0)
        self.modeButtons.addButton(shots, id=1)
        self.modeButtons.addButton(heatmap, id=2)
        self.modeButtons.setExclusive(False)
        self.modeButtons.buttonClicked.connect(self.boxChecked)
        hLayout.addWidget(passes)
        hLayout.addWidget(shots)
        hLayout.addWidget(heatmap)

        # create pitch widget
        self.pitch = PitchWidget(config["Pitch"])
        
        vLayout.addLayout(hLayout)
        vLayout.addWidget(self.pitch)

    def boxChecked(self,object):
        """Toggles options in the pitch widget, based on
        which box is checked.

        Args:
            object ([type]): [description]
        """
        if self.modeButtons.id(object) == 0:
            self.pitch.showPasses = False if self.pitch.showPasses else True
        if self.modeButtons.id(object) == 1:
            self.pitch.showShots = False if self.pitch.showShots else True
        if self.modeButtons.id(object) == 2:
            self.pitch.showHeatmap = False if self.pitch.showHeatmap else True
        
        self.pitch.update()

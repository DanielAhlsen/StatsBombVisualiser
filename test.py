#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from VisualiserWidget import VisualiserWidget
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication
import sys

def main(argv):
    with open("./config.json") as f:
        config = json.load(f)

    app = QApplication(sys.argv)
    w = VisualiserWidget(config["Visualiser"])

    w.show()
    app.exec()



if __name__=='__main__':
    main(sys.argv)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtGui import QPolygon
from PyQt5.QtCore import QLine, QPoint
from math import atan2, pi, sin, cos

def drawArrow(painter,x0,y0,x1,y1,arrowsize,tip_angle = pi/3):
    """Draws an arrow using the painter.

    Args:
        painter (QPainter): The painter used for drawing
        x0 (int): x-coordinate of the start point.
        y0 (int): y-coordinate of the start point.
        x1 (int): x-coordinate of the end point.
        y1 (int): y-coordinate of the end point
        arrowsize (int): size of the arrow head in pixels.
        tip_angle (float, optional): Angle of the arrow head. Defaults to pi/3.
    """
    tip_angle = pi/3 if not tip_angle else tip_angle
    line = QLine(x0,y0,x1,y1)
    angle = atan2(-line.dy(), line.dx())
    arrowpoint1 = line.p2()-QPoint(sin(angle+tip_angle)*arrowsize,
                         cos(angle+tip_angle)*arrowsize)
    arrowpoint2 = line.p2()-QPoint(sin(angle+pi-tip_angle)*arrowsize,
                         cos(angle+pi-tip_angle)*arrowsize)

    arrowhead = QPolygon()
    arrowhead << line.p2() << arrowpoint1 << arrowpoint2

    painter.drawLine(line)
    painter.drawPolygon(arrowhead)
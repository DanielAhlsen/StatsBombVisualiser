#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (
    QGraphicsScene, 
    QGraphicsRectItem, 
    QGraphicsEllipseItem, 
    QGraphicsLineItem
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen

PITCH_DIMENSION_LIMITS = { 
    'metric' : {
        'MAX_LENGTH' : 120.0,
        'MIN_LENGTH' : 90.0,
        'MAX_WIDTH' : 90.0,
        'MIN_WIDTH' : 45.0
    },
    'imperial' : {
        'MAX_LENGTH' : 130.0,
        'MIN_LENGTH' : 100.0,
        'MAX_WIDTH' : 100.0,
        'MIN_WIDTH' : 50.0
    }
}
PITCH_DIMENSIONS = { 'metric' : {
    'PENALTY_SPOT' : 11.0,
    'GOAL_WIDTH' : 7.32,
    'PENALTY_BOX_DEPTH' : 16.5,
    'PENALTY_BOX_WIDTH' : 40.3,
    'GOAL_AREA_DEPTH' : 5.5,
    'GOAL_AREA_WIDTH' : 18.32,
    'CENTER_CIRCLE_RADIUS' : 9.15,
    'PENALTY_KICK_CIRCLE' : 9.15,
    'PENALTY_SPOT_RADIUS' : 0.11,
    'CORNER_CIRCLE' : 9.15,
    'CORNER_ARC_RADIUS' : 0.92,
    },
    'imperial' : {
    'PENALTY_SPOT' : 12.0,
    'GOAL_WIDTH' : 8.0,
    'PENALTY_BOX_DEPTH' : 20.0,
    'PENALTY_BOX_WIDTH' : 44.0,
    'CENTER_CIRCLE_RADIUS' : 10.0,
    'GOAL_AREA_DEPTH' : 6.0,
    'GOAL_AREA_WIDTH' : 20.0,
    'PENALTY_KICK_CIRCLE' : 10.0,
    'PENALTY_SPOT_RADIUS' : 0.125,
    'CORNER_CIRCLE' : 10.0,
    'CORNER_ARC_RADIUS' : 1.0,
    }
}

class PitchScene(QGraphicsScene):

    def __init__(self,x_origin,y_origin,x_len,y_len,x_pad,y_pad,pitch_length,pitch_width,pen,brush_dark,brush_light,brush_background,n_stripes,mode,parent=None):
        super().__init__(x_origin,y_origin,x_len,y_len,parent)
        self.setSceneRect(0,0,x_len,y_len)
        self.setBackgroundBrush(brush_background)
        # set mode to metric or imperial
        if not mode == 'metric' or mode == 'imperial':
            raise ValueError("Mode must be \'imperial\' or \'metric\'.")
        
        self.mode = mode

        # check if pitch dimensions are correct
        if pitch_length < PITCH_DIMENSION_LIMITS[mode]['MIN_LENGTH'] or pitch_length > PITCH_DIMENSION_LIMITS[mode]['MAX_LENGTH']:
            if mode == 'metric':
                raise ValueError("In metric mode, pitch length must be between 90m and 120m.")
            if mode == 'imperial':
                raise ValueError("In imperial mode, pitch length must be between 100 yards and 130 yards.")
        if pitch_width < PITCH_DIMENSION_LIMITS[mode]['MIN_WIDTH'] or pitch_width > PITCH_DIMENSION_LIMITS[mode]['MAX_WIDTH']:
            if mode == 'metric':
                raise ValueError("In metric mode, pitch width must be between 45m and 90m.")
            if mode == 'imperial':
                raise ValueError("In imperial mode, pitch width must be between 50 yards and 100 yards.")

        self.pitch_width = pitch_width
        self.pitch_length = pitch_length
        self.n_stripes = n_stripes
        self.pen = pen
        self.x_pad = x_pad
        self.y_pad = y_pad
        self.dark_brush = brush_dark
        self.light_brush = brush_light

        # normalise measurements so that the length of the pitch is 1.0
        self.relative_pitch_measurements = { k : v/pitch_length for k,v in PITCH_DIMENSIONS[mode].items() }
        self.relative_pitch_measurements["PITCH_LENGTH"] = 1.0
        self.relative_pitch_measurements["PITCH_WIDTH"] = pitch_width/pitch_length
                

    def drawPitch(self):
        # choose whether to use x_pad or y_pad
        if self.pitch_length/self.pitch_width > self.width()/self.height():
            factor = self.width()-2*self.x_pad
        else:
            factor = (self.height()-2*self.y_pad)/self.relative_pitch_measurements["PITCH_WIDTH"]

        # find measurements
        meas = { k : v*factor for k,v in self.relative_pitch_measurements.items() }

        # adjust for padding

        if self.pitch_length/self.pitch_width <= self.width()/self.height():
            p = (self.x_pad,int(self.height()/2-meas["PITCH_WIDTH"]/2))
        else:
            p = (int(self.width()/2-meas["PITCH_LENGTH"]/2),self.y_pad)

        rect_points = {}
        ellipse_points = {}
        line_points = {}

        rect_points["PITCH"] = ((0,0),(int(meas["PITCH_LENGTH"]),int(meas["PITCH_WIDTH"])))

        rect_points["LEFT_PENALTY_BOX"] = ((0,int(meas["PITCH_WIDTH"]/2-meas["PENALTY_BOX_WIDTH"]/2)),
                                    (int(meas["PENALTY_BOX_DEPTH"]),int(meas["PITCH_WIDTH"]/2+meas["PENALTY_BOX_WIDTH"]/2)))

        rect_points["LEFT_GOAL_AREA"] = ((0,int(meas["PITCH_WIDTH"]/2-meas["GOAL_AREA_WIDTH"]/2)),
                                    (int(meas["GOAL_AREA_DEPTH"]),int(meas["PITCH_WIDTH"]/2+meas["GOAL_AREA_WIDTH"]/2)))

        ellipse_points["LEFT_PENALTY_CIRCLE"] = ((int(meas["PENALTY_SPOT"]-meas["PENALTY_KICK_CIRCLE"]),int(meas["PITCH_WIDTH"]/2-meas["PENALTY_KICK_CIRCLE"])),
                                    (int(meas["PENALTY_SPOT"]+meas["PENALTY_KICK_CIRCLE"]),int(meas["PITCH_WIDTH"]/2+meas["PENALTY_KICK_CIRCLE"])))

        ellipse_points["LEFT_PENALTY_SPOT"] = ((int(meas["PENALTY_SPOT"]-meas["PENALTY_SPOT_RADIUS"]),int(meas["PITCH_WIDTH"]/2-meas["PENALTY_SPOT_RADIUS"])),
                                    (int(meas["PENALTY_SPOT"]+meas["PENALTY_SPOT_RADIUS"]),int(meas["PITCH_WIDTH"]/2+meas["PENALTY_SPOT_RADIUS"])))

        ellipse_points["UPPER_LEFT_CORNER"] = ((int(-meas["CORNER_ARC_RADIUS"]),int(-meas["CORNER_ARC_RADIUS"])),
                                    (int(meas["CORNER_ARC_RADIUS"]),int(meas["CORNER_ARC_RADIUS"])))

        ellipse_points["LOWER_LEFT_CORNER"] = ((int(-meas["CORNER_ARC_RADIUS"]),int(meas["PITCH_WIDTH"]-meas["CORNER_ARC_RADIUS"])),
                                    (int(meas["CORNER_ARC_RADIUS"]),int(meas["PITCH_WIDTH"]+meas["CORNER_ARC_RADIUS"])))

        line_points["HALFWAY_LINE"] = ((int(meas["PITCH_LENGTH"]/2),0),
                                    (int(meas["PITCH_LENGTH"]/2),int(meas["PITCH_WIDTH"])))

        ellipse_points["CENTER_CIRCLE"] = ((int(meas["PITCH_LENGTH"]/2-meas["CENTER_CIRCLE_RADIUS"]),int(meas["PITCH_WIDTH"]/2-meas["CENTER_CIRCLE_RADIUS"])),
                                    (int(meas["PITCH_LENGTH"]/2+meas["CENTER_CIRCLE_RADIUS"]),int(meas["PITCH_WIDTH"]/2+meas["CENTER_CIRCLE_RADIUS"])))

        rect_points["RIGHT_PENALTY_BOX"] = ((int(meas["PITCH_LENGTH"]-meas["PENALTY_BOX_DEPTH"]),int(meas["PITCH_WIDTH"]/2-meas["PENALTY_BOX_WIDTH"]/2)),
                                    (int(meas["PITCH_LENGTH"]),int(meas["PITCH_WIDTH"]/2+meas["PENALTY_BOX_WIDTH"]/2)))

        rect_points["RIGHT_GOAL_AREA"] = ((int(meas["PITCH_LENGTH"]-meas["GOAL_AREA_DEPTH"]),int(meas["PITCH_WIDTH"]/2-meas["GOAL_AREA_WIDTH"]/2)),
                                    (int(meas["PITCH_LENGTH"]),int(meas["PITCH_WIDTH"]/2+meas["GOAL_AREA_WIDTH"]/2)))

        ellipse_points["RIGHT_PENALTY_CIRCLE"] = ((int(meas["PITCH_LENGTH"]-meas["PENALTY_SPOT"]-meas["PENALTY_KICK_CIRCLE"]),int(meas["PITCH_WIDTH"]/2-meas["PENALTY_KICK_CIRCLE"])),
                                    (int(meas["PITCH_LENGTH"]-meas["PENALTY_SPOT"]+meas["PENALTY_KICK_CIRCLE"]),int(meas["PITCH_WIDTH"]/2+meas["PENALTY_KICK_CIRCLE"])))
    
        ellipse_points["RIGHT_PENALTY_SPOT"] = ((int(meas["PITCH_LENGTH"]-meas["PENALTY_SPOT"]-meas["PENALTY_SPOT_RADIUS"]),int(meas["PITCH_WIDTH"]/2-meas["PENALTY_SPOT_RADIUS"])),
                                    (int(meas["PITCH_LENGTH"]-meas["PENALTY_SPOT"]+meas["PENALTY_SPOT_RADIUS"]),int(meas["PITCH_WIDTH"]/2+meas["PENALTY_SPOT_RADIUS"])))

        ellipse_points["UPPER_RIGHT_CORNER"] = ((int(meas["PITCH_LENGTH"]-meas["CORNER_ARC_RADIUS"]),int(-meas["CORNER_ARC_RADIUS"])),
                                    (int(meas["PITCH_LENGTH"]+meas["CORNER_ARC_RADIUS"]),int(meas["CORNER_ARC_RADIUS"])))

        ellipse_points["LOWER_RIGHT_CORNER"] = ((int(meas["PITCH_LENGTH"]-meas["CORNER_ARC_RADIUS"]),int(meas["PITCH_WIDTH"]-meas["CORNER_ARC_RADIUS"])),
                                    (int(meas["PITCH_LENGTH"]+meas["CORNER_ARC_RADIUS"]),int(meas["PITCH_WIDTH"]+meas["CORNER_ARC_RADIUS"])))

        rects = {}
        ellipses = {}
        lines = {}
        stripes = []

        for k,v in rect_points.items():
            rects[k] = QGraphicsRectItem(v[0][0],v[0][1],v[1][0]-v[0][0],v[1][1]-v[0][1])
            rects[k].setPen(self.pen)

        for k,v in ellipse_points.items():
            ellipses[k] = QGraphicsEllipseItem( v[0][0],v[0][1],v[1][0]-v[0][0],v[1][1]-v[0][1])
            ellipses[k].setPen(self.pen)

        for k,v in line_points.items():
            lines[k] = QGraphicsLineItem(v[0][0],v[0][1],v[1][0],v[1][1])
            lines[k].setPen(self.pen)

        ellipses["LEFT_PENALTY_CIRCLE"].setStartAngle(5760-850)
        ellipses["LEFT_PENALTY_CIRCLE"].setSpanAngle(850*2)

        ellipses["RIGHT_PENALTY_CIRCLE"].setStartAngle(2880-850)
        ellipses["RIGHT_PENALTY_CIRCLE"].setSpanAngle(850*2)

        ellipses["UPPER_LEFT_CORNER"].setSpanAngle(1440)
        ellipses["LOWER_LEFT_CORNER"].setSpanAngle(1440)
        ellipses["UPPER_RIGHT_CORNER"].setSpanAngle(1440)
        ellipses["LOWER_RIGHT_CORNER"].setSpanAngle(1440)

        ellipses["UPPER_LEFT_CORNER"].setStartAngle(4320)
        ellipses["LOWER_LEFT_CORNER"].setStartAngle(0)
        ellipses["UPPER_RIGHT_CORNER"].setStartAngle(2880)
        ellipses["LOWER_RIGHT_CORNER"].setStartAngle(1440)

        if self.n_stripes >= 1:
            length = int(meas["PITCH_LENGTH"])
            stripe_lens = [ int(length/self.n_stripes) for _ in range(self.n_stripes)]
            rem = length % self.n_stripes
            i = rem
            while True:
                if i < 1:
                    break
                stripe_lens[i] += 1
                i += -1
                if i < 1:
                    break
                stripe_lens[-1-i] +=1
                i += -1

            stripe_points = []
            acc = 0

            for i in range(len(stripe_lens)):
                stripe_points.append(((acc,0),(acc+stripe_lens[i],int(meas["PITCH_WIDTH"]))))
                acc += stripe_lens[i]

            for i in range(len(stripe_points)):
                stripes.append(QGraphicsRectItem(stripe_points[i][0][0],stripe_points[i][0][1],stripe_points[i][1][0]-stripe_points[i][0][0],stripe_points[i][1][1]-stripe_points[i][0][1]))
                stripes[i].setPen(QPen(Qt.NoPen))
                if i % 2 == 1:
                    stripes[i].setBrush(self.dark_brush)
                if i % 2 == 0:
                    stripes[i].setBrush(self.light_brush)
            
            for v in stripes:
                v.moveBy(p[0],p[1])
                self.addItem(v)

        for v in rects.values():
            v.moveBy(p[0],p[1])
            self.addItem(v)

        for v in ellipses.values():
            v.moveBy(p[0],p[1])
            self.addItem(v)

        for v in lines.values():
            v.moveBy(p[0],p[1])
            self.addItem(v)
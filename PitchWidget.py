from PyQt5.QtWidgets import (
    QWidget
)
from PyQt5.QtGui import QBrush, QPalette, QPen, QPainter, QColor
from PyQt5.QtCore import QRect, QLine, Qt
from PaintingUtilities import drawArrow

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
    'GOAL_DEPTH' : 2.74,
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
    'GOAL_DEPTH' : 3.0,
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

def getCircleRect(radius,midpoint):
    return QRect(int(midpoint[0]-radius),int(midpoint[1]-radius),
                 int(2*radius),int(2*radius))

class PitchWidget(QWidget):

    def __init__(self,config,parent = None):
        super().__init__(parent)
        
        self.setGeometry(config["x_origin"],config["y_origin"],
                         config["window_width"],config["window_height"])

        self.unit = config["unit"]
        self.length = config["pitch_length"]
        self.width = config["pitch_width"]
        self.n_stripes = config["n_stripes"]
        self.x_pad = config["x_padding"]
        self.y_pad = config["y_padding"]

        self.marking_pen = QPen()
        self.marking_color = QColor(config["marking_color"])
        self.marking_width = config["marking_width"]
        self.background_color = QColor(config["background_color"])

        self.even_stripe_color = QColor(config["light_color"])
        self.odd_stripe_color = QColor(config["dark_color"])

        self.showPasses = config["show_passes"]
        self.showShots = config["show_shots"]
        self.showHeatmap = config["show_heatmap"]

    @property
    def length(self):
        """The length of the football pitch."""
        return self._length
    @length.setter
    def length(self, value):
        # check if pitch dimensions are correct
        if(value < PITCH_DIMENSION_LIMITS[self.unit]['MIN_LENGTH'] or        
                value > PITCH_DIMENSION_LIMITS[self.unit]['MAX_LENGTH']):
            if self.unit == 'metric':
                raise ValueError("In metric units, pitch length must be \
                    between 90m and 120m.")
            if self.unit == 'imperial':
                raise ValueError("In imperial units, pitch length must be \
                    between 100yd and 130yd.")
        self._length = value

        # A name error will occur when the class is initialized.
        try:
            self.calculateRelativePitchDimensions()
        except AttributeError:
            pass

    @property
    def width(self):
        """The width of the football pitch."""
        return self._width
    @width.setter
    def width(self, value):
        if(value < PITCH_DIMENSION_LIMITS[self.unit]['MIN_WIDTH'] or 
                value > PITCH_DIMENSION_LIMITS[self.unit]['MAX_WIDTH']):
            if value == 'metric':
                raise ValueError("In metric units, pitch width must be \
                    between 45m and 90m.")
            if value == 'imperial':
                raise ValueError("In imperial unit, pitch width must be \
                    between 50 yd and 100 yd.")
        self._width = value

        # A name error can occur when the class is initialized.
        try:
            self.calculateRelativePitchDimensions()
        except AttributeError:
            pass

    @property
    def unit(self):
        """The system of units used specify the pitch dimensions."""
        return self._unit
    @unit.setter
    def unit(self, value):
        if not value == 'metric' and not value == 'imperial':
            raise ValueError("Mode must be \'imperial\' or \'metric\'.")
        self._unit = value

    @property
    def stripes(self):
        """The number of stripes on the field."""
        return self._stripes
    @stripes.setter
    def stripes(self, value):
        if value < 0:
            raise ValueError("Number of stripes must not be negative")
        self._stripes = value

    @property
    def x_pad(self):
        """The minimum horizontal padding."""
        return self._x_pad
    @x_pad.setter
    def x_pad(self, value):
        if value < 0:
            raise ValueError("Horizontal padding must not be negative")
        self._x_pad = value

    @property
    def y_pad(self):
        """The minimum vertical padding."""
        return self._y_pad
    @y_pad.setter
    def y_pad(self, value):
        if value < 0:
            raise ValueError("Vertical padding must not be negative")
        self._y_pad = value

    @property
    def marking_pen(self):
        """The pen used to draw pitch markings."""
        return self._marking_pen
    @marking_pen.setter
    def marking_pen(self, value):
        self._marking_pen = value

    @property
    def marking_color(self):
        """The color of the marking pen."""
        return self._marking_pen.color()
    @marking_color.setter
    def marking_color(self, value):
        self._marking_pen.setColor(value)

    @property
    def marking_width(self):
        """The width of the pitch markings in pixels."""
        return self._marking_pen.width()
    @marking_width.setter
    def marking_width(self, value):
        self._marking_pen.setWidth(value)

    @property
    def background_color(self):
        """The background color of the widget."""
        return self.palette().brush(QPalette.Window).color()
    @background_color.setter
    def background_color(self, value):
        palette = QPalette()
        palette.setBrush(QPalette.Window,QBrush(value))
        self.setPalette(palette)
        self.setAutoFillBackground(True)
        self.update()

    @property
    def even_stripe_color(self):
        """The even_stripe_color property."""
        return self._even_stripe_color
    @even_stripe_color.setter
    def even_stripe_color(self, value):
        self._even_stripe_color = value

    @property
    def odd_stripe_color(self):
        """The odd_stripe_color property."""
        return self._odd_stripe_color
    @odd_stripe_color.setter
    def odd_stripe_color(self, value):
        self._odd_stripe_color = value

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        self.drawPitch(painter)
        if self.showPasses:
            painter.setPen((self.marking_pen))
            painter.setBrush(QBrush(Qt.NoBrush))
            drawArrow(painter,0,0,120,120,10)
        painter.end()
        return super().paintEvent(event)

    def drawPitch(self,painter):

        f, p = self.calculatePadding()
        abs_meas = { k : v*f for k,v in self.rel_dim.items()}

        if abs_meas["PENALTY_SPOT_RADIUS"] < 1:
            abs_meas["PENALTY_SPOT_RADIUS"] = 1

        
        self.drawStripes(p,abs_meas,painter)

        painter.setPen((self.marking_pen))
        painter.setBrush(QBrush(Qt.NoBrush))

        self.drawRects(p,abs_meas,painter)
        self.drawArcs(p,abs_meas,painter)
        self.drawLines(p,abs_meas,painter)

    def drawStripes(self,p,abs_meas,painter):
        """ Draws the stripes on the field

        Args:
            p (int,int): Padding used for drawing
            length (int): The length of the pitch
            height ([type]): The height (width) of the pitch
            painter ([type]): [description]
        """
        # Calculate offside stripes on the fields

        length = int(abs_meas["PITCH_LENGTH"])
        height = int(abs_meas["PITCH_WIDTH"])
        r = length%self.n_stripes
        s = (self.n_stripes-r) // 2
        w = [ length // self.n_stripes for _ in range(self.n_stripes) ]

        for i in range(r):
            w[s+i] += 1

        s = 0
        widths = [0]
        for i in range(self.n_stripes):
            s += w[i]
            widths.append(s)

        # Draw stripes
        painter.setPen(Qt.NoPen)

        for i in range(self.n_stripes):
            if i % 2 == 0:
                painter.setBrush(QBrush(self.even_stripe_color))
                painter.drawRect(QRect(p[0]+widths[i], p[1], w[i], height))
            if i % 2 == 1:
                painter.setBrush(QBrush(self.odd_stripe_color))
                painter.drawRect(QRect(p[0]+widths[i], p[1], w[i], height))

    def drawRects(self,p,abs_meas,painter):

        # Draw the pitch
        painter.drawRect(QRect(p[0],
                               p[1],
                               int(abs_meas["PITCH_LENGTH"]),
                               int(abs_meas["PITCH_WIDTH"])))

        # Draw left penalty box
        painter.drawRect(QRect(p[0],
                                p[1]+int((abs_meas["PITCH_WIDTH"]
                                - abs_meas["PENALTY_BOX_WIDTH"])/2),
                                int(abs_meas["PENALTY_BOX_DEPTH"]),
                                int(abs_meas["PENALTY_BOX_WIDTH"])))
        
        # Draw left goal area
        painter.drawRect(QRect(p[0],
                             p[1]+int((abs_meas["PITCH_WIDTH"]
                            -abs_meas["GOAL_AREA_WIDTH"])/2),
                             int(abs_meas["GOAL_AREA_DEPTH"]),
                             int(abs_meas["GOAL_AREA_WIDTH"])))
        
        # Draw left goal
        painter.drawRect(QRect(p[0]-int(abs_meas["GOAL_DEPTH"]),
                               p[1]+int((abs_meas["PITCH_WIDTH"]
                               -abs_meas["GOAL_WIDTH"])/2),
                               int(abs_meas["GOAL_DEPTH"]),
                               int(abs_meas["GOAL_WIDTH"])))

        # Draw right penalty box
        painter.drawRect(QRect(abs_meas["PITCH_LENGTH"]+p[0]
                               -int(abs_meas["PENALTY_BOX_DEPTH"]),
                               p[1]+int((abs_meas["PITCH_WIDTH"]
                                -abs_meas["PENALTY_BOX_WIDTH"])/2),
                               int(abs_meas["PENALTY_BOX_DEPTH"]),
                               int(abs_meas["PENALTY_BOX_WIDTH"])))

        # Draw right goal area
        painter.drawRect(QRect(abs_meas["PITCH_LENGTH"]+p[0]
                            -int(abs_meas["GOAL_AREA_DEPTH"]),
                             p[1]+int((abs_meas["PITCH_WIDTH"]
                            -abs_meas["GOAL_AREA_WIDTH"])/2),
                             int(abs_meas["GOAL_AREA_DEPTH"]),
                             int(abs_meas["GOAL_AREA_WIDTH"])))

        # Draw right goal
        painter.drawRect(QRect(abs_meas["PITCH_LENGTH"]+p[0],
                             p[1]+int((abs_meas["PITCH_WIDTH"]
                            -abs_meas["GOAL_WIDTH"])/2),
                             int(abs_meas["GOAL_DEPTH"]),
                             int(abs_meas["GOAL_WIDTH"])))

    def drawArcs(self,p,abs_meas,painter):
        frame_width = self.geometry().width()

        # Draw the centre circle
        painter.drawEllipse(getCircleRect(abs_meas["CENTER_CIRCLE_RADIUS"],
                                      (p[0]+abs_meas["PITCH_LENGTH"]/2,
                                        p[1]+abs_meas["PITCH_WIDTH"]/2)))

        # Draw left penalty box arc
        painter.drawArc(getCircleRect(abs_meas["PENALTY_KICK_CIRCLE"],
                                       (p[0]+abs_meas["PENALTY_SPOT"],
                                            p[1]+abs_meas["PITCH_WIDTH"]/2)),
                                        4910,1700)

        # Draw right penalty box arc
        painter.drawArc(getCircleRect(abs_meas["PENALTY_KICK_CIRCLE"],
                                        (frame_width-p[0]
                                        -abs_meas["PENALTY_SPOT"],
                                            p[1]+abs_meas["PITCH_WIDTH"]/2)),
                                        2030,1700)

        # Make sure the penalty spots are filled
        painter.setBrush(QBrush(self.marking_color))

        # Draw left penalty spot
        painter.drawEllipse(getCircleRect(abs_meas["PENALTY_SPOT_RADIUS"],
                                          (p[0]+abs_meas["PENALTY_SPOT"],
                                            p[1]+abs_meas["PITCH_WIDTH"]/2)))

        # Draw right penalty spot
        painter.drawEllipse(getCircleRect(abs_meas["PENALTY_SPOT_RADIUS"],
                                        (frame_width-p[0]
                                        -abs_meas["PENALTY_SPOT"],
                                        p[1]+abs_meas["PITCH_WIDTH"]/2)))
        
    def drawLines(self,p,abs_meas,painter):
        # Draw halfway line
        painter.drawLine(QLine(p[0]+int(abs_meas["PITCH_LENGTH"]/2),
                             p[1],
                             p[0]+int(abs_meas["PITCH_LENGTH"]/2),
                             p[1]+int(abs_meas["PITCH_WIDTH"])))
    
    def drawPasses(self,p,abs_meas,painter):
        pass

    def drawShots(self,p,abs_meas,painter):
        pass

    def calculatePadding(self):
        """Calculate the scaling factor and padding for rendering the pitch.

        Returns:
            float, (int,int): Scaling factor and tuple of paddings.
        """
        rel_length = self.rel_dim["PITCH_LENGTH"]
        rel_width = self.rel_dim["PITCH_WIDTH"]

        frame_width = self.geometry().width()
        frame_height = self.geometry().height()
        q = frame_height/frame_width
        if q <= rel_width:
            yp = self.y_pad
            f = (frame_height-2*yp)/rel_width
            xp = int((frame_width-rel_length*f)/2)
        else:
            xp = self.x_pad
            f = (frame_width-2*xp)/rel_length
            yp = int((frame_height-rel_width*f)/2)

        #gd = int(f*self.rel_dim["GOAL_DEPTH"])
        return f, (xp,yp)

    def calculateRelativePitchDimensions(self):
        x = self.length+2*PITCH_DIMENSIONS[self.unit]["GOAL_DEPTH"]
        self.rel_dim = { k : v/x for 
                    k,v in PITCH_DIMENSIONS[self.unit].items()}
        self.rel_dim["PITCH_LENGTH"] = self.length/x
        self.rel_dim["PITCH_WIDTH"] = self.width/x
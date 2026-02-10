from qtpy.QtWidgets import QCheckBox
from qtpy.QtCore import Qt, QPropertyAnimation, Property, QPoint, QEasingCurve, QRect
from qtpy.QtGui import QPainter, QColor, QBrush, QPen

class Switch(QCheckBox):
    def __init__(self, parent=None, track_radius=10, thumb_radius=8):
        super().__init__(parent)
        self.setFixedSize(50, 30)
        self.setCursor(Qt.PointingHandCursor)
        
        # Colors
        self._track_color_off = QColor("#334155") # Slate-700
        self._track_color_on = QColor("#8b5cf6")  # Purple-500
        self._thumb_color = QColor("#f8fafc")     # Slate-50
        
        self._thumb_pos = 3.0
        
        self._animation = QPropertyAnimation(self, b"thumb_pos", self)
        self._animation.setDuration(200)
        self._animation.setEasingCurve(QEasingCurve.InOutQuad)
        
        self.stateChanged.connect(self._handle_state_change)

    @Property(float)
    def thumb_pos(self):
        return self._thumb_pos

    @thumb_pos.setter
    def thumb_pos(self, pos):
        self._thumb_pos = pos
        self.update()

    def _handle_state_change(self, state):
        start = self._thumb_pos
        end = self.width() - 27 if self.isChecked() else 3
        self._animation.setStartValue(start)
        self._animation.setEndValue(float(end))
        self._animation.start()

    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        # Draw Track
        track_color = self._track_color_on if self.isChecked() else self._track_color_off
        painter.setBrush(QBrush(track_color))
        painter.drawRoundedRect(0, 0, self.width(), self.height(), self.height()/2, self.height()/2)

        # Draw Thumb
        painter.setBrush(QBrush(self._thumb_color))
        y_pos = (self.height() - 24) / 2
        painter.drawEllipse(int(self._thumb_pos), int(y_pos), 24, 24)

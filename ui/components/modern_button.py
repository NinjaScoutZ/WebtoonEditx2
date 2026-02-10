"""
Modern Button Components with Animations
"""
from qtpy.QtWidgets import QPushButton, QToolButton, QWidget, QGraphicsDropShadowEffect
from qtpy.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QSize
from qtpy.QtGui import QColor, QIcon, QPainter, QPaintEvent


class ModernButton(QPushButton):
    """Modern Styled Button with Hover Animation"""
    
    def __init__(self, text: str = "", parent=None, primary: bool = False):
        super().__init__(text, parent)
        self._primary = primary
        self._scale = 1.0
        self._setup_style()
        self._setup_animation()
    
    def _setup_style(self):
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(36)
        if self._primary:
            self.setObjectName("PrimaryButton")
    
    def _setup_animation(self):
        self._anim = QPropertyAnimation(self, b"scale")
        self._anim.setDuration(150)
        self._anim.setEasingCurve(QEasingCurve.OutCubic)
    
    def enterEvent(self, event):
        self._anim.setStartValue(1.0)
        self._anim.setEndValue(1.02)
        self._anim.start()
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        self._anim.setStartValue(self._scale)
        self._anim.setEndValue(1.0)
        self._anim.start()
        super().leaveEvent(event)
    
    @Property(float)
    def scale(self):
        return self._scale
    
    @scale.setter
    def scale(self, value):
        self._scale = value
        self.update()


class ModernIconButton(QToolButton):
    """Modern Icon Button for Toolbars"""
    
    def __init__(self, icon_path: str = "", tooltip: str = "", parent=None, checkable: bool = False):
        super().__init__(parent)
        self.setToolTip(tooltip)
        self.setCheckable(checkable)
        self._setup_style()
        
        if icon_path:
            self.setIcon(QIcon(icon_path))
    
    def _setup_style(self):
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedSize(40, 40)
        self.setIconSize(QSize(24, 24))
        self.setAutoRaise(True)


class ModernToggleButton(ModernIconButton):
    """Toggle Button with Active State Indicator"""
    
    def __init__(self, icon_path: str = "", tooltip: str = "", parent=None):
        super().__init__(icon_path, tooltip, parent, checkable=True)
        self._active_color = QColor("#6366f1")
        self._inactive_color = QColor("transparent")
    
    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw background
        if self.isChecked():
            painter.setBrush(self._active_color)
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(self.rect().adjusted(4, 4, -4, -4), 8, 8)
        
        painter.end()
        super().paintEvent(event)

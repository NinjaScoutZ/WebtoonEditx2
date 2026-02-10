"""
Modern Button Components with Animations
"""
from qtpy.QtWidgets import QPushButton, QToolButton, QWidget, QGraphicsDropShadowEffect
from qtpy.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QSize
from qtpy.QtGui import QColor, QIcon, QPainter, QPaintEvent


class ModernButton(QPushButton):
    """Modern Styled Button with Hover Animation and Refined Style"""
    
    def __init__(self, text: str = "", parent=None, primary: bool = False):
        super().__init__(text, parent)
        self._primary = primary
        self._scale = 1.0
        self._setup_style()
        self._setup_animation()
    
    def _setup_style(self):
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(40)
        self.setStyleSheet("""
            QPushButton {
                border-radius: 12px;
                font-weight: 600;
                letter-spacing: 0.5px;
            }
        """)
        if self._primary:
            self.setObjectName("PrimaryButton")
    
    def _setup_animation(self):
        self._anim = QPropertyAnimation(self, b"scale")
        self._anim.setDuration(100)
        self._anim.setEasingCurve(QEasingCurve.OutQuad)
    
    def enterEvent(self, event):
        self._anim.setStartValue(self._scale)
        self._anim.setEndValue(1.05)
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
    """Modern Icon Button with Circle Background on Hover"""
    
    def __init__(self, icon_path: str = "", tooltip: str = "", parent=None, checkable: bool = False):
        super().__init__(parent)
        self.setToolTip(tooltip)
        self.setCheckable(checkable)
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedSize(40, 40)
        self.setIconSize(QSize(22, 22))
        self.setAutoRaise(True)
        self.setStyleSheet("""
            QToolButton {
                border-radius: 20px;
                background-color: transparent;
                border: none;
            }
            QToolButton:hover {
                background-color: rgba(255, 255, 255, 0.08);
            }
            QToolButton:checked {
                background-color: #6366f1;
                color: white;
            }
        """)

        if icon_path:
            self.setIcon(QIcon(icon_path))


class ModernToggleButton(ModernIconButton):
    """Toggle Button with Active State Indicator"""
    
    def __init__(self, icon_path: str = "", tooltip: str = "", parent=None):
        super().__init__(icon_path, tooltip, parent, checkable=True)

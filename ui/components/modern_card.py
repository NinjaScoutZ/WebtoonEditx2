"""
Modern Card Component with Animations
"""
from qtpy.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGraphicsDropShadowEffect
from qtpy.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property
from qtpy.QtGui import QColor


class ModernCard(QWidget):
    """Modern Card with Shadow and Hover Lift Effect"""
    
    def __init__(self, title: str = "", parent=None):
        super().__init__(parent)
        self._title = title
        self._setup_ui()
        self._setup_shadow()
        self._setup_animation()
    
    def _setup_ui(self):
        self.setObjectName("ModernCard")
        self.setAttribute(Qt.WA_StyledBackground, True)
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(16, 16, 16, 16)
        self.main_layout.setSpacing(12)
        
        if self._title:
            self.title_label = QLabel(self._title)
            self.title_label.setObjectName("CardTitle")
            self.main_layout.addWidget(self.title_label)
    
    def _setup_shadow(self):
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setColor(QColor(0, 0, 0, 80))
        self.shadow.setOffset(0, 4)
        self.setGraphicsEffect(self.shadow)

    def _setup_animation(self):
        self._anim = QPropertyAnimation(self.shadow, b"blurRadius")
        self._anim.setDuration(200)

    def enterEvent(self, event):
        self._anim.setEndValue(30)
        self._anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._anim.setEndValue(20)
        self._anim.start()
        super().leaveEvent(event)
    
    def set_content(self, widget: QWidget):
        self.main_layout.addWidget(widget)
    
    def add_widget(self, widget: QWidget):
        self.main_layout.addWidget(widget)

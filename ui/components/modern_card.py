"""
Modern Card Component
"""
from qtpy.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGraphicsDropShadowEffect
from qtpy.QtCore import Qt
from qtpy.QtGui import QColor


class ModernCard(QWidget):
    """Modern Card with Shadow Effect"""
    
    def __init__(self, title: str = "", parent=None):
        super().__init__(parent)
        self._title = title
        self._setup_ui()
        self._setup_shadow()
    
    def _setup_ui(self):
        self.setObjectName("ModernCard")
        self.setAttribute(Qt.WA_StyledBackground, True)
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(16, 16, 16, 16)
        self.main_layout.setSpacing(12)
        
        if self._title:
            self.title_label = QLabel(self._title)
            self.title_label.setObjectName("CardTitle")
            self.title_label.setStyleSheet("""
                font-size: 14px;
                font-weight: 600;
                color: #f8fafc;
            """)
            self.main_layout.addWidget(self.title_label)
    
    def _setup_shadow(self):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 60))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)
    
    def set_content(self, widget: QWidget):
        """Set main content widget"""
        self.main_layout.addWidget(widget)
    
    def add_widget(self, widget: QWidget):
        """Add widget to card"""
        self.main_layout.addWidget(widget)
    
    def add_layout(self, layout):
        """Add layout to card"""
        self.main_layout.addLayout(layout)

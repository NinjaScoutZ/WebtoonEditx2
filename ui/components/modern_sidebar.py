"""
Modern Sidebar Component
"""
from qtpy.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QToolButton, 
    QLabel, QSpacerItem, QSizePolicy, QFrame, QScrollArea
)
from qtpy.QtCore import Qt, Signal, QSize
from qtpy.QtGui import QIcon, QPainter, QColor, QPaintEvent, QPen
import os.path as osp


class SidebarButton(QToolButton):
    """Modern Sidebar Button with Active Indicator"""
    
    def __init__(self, icon_name: str, text: str, parent=None, checkable: bool = False):
        super().__init__(parent)
        self._icon_name = icon_name
        self._text = text
        
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.setIconSize(QSize(24, 24))
        self.setCheckable(checkable)
        self.setAutoRaise(True)
        self.setFixedSize(56, 56)
        self.setCursor(Qt.PointingHandCursor)
        self.setToolTip(text)
        
        self._setup_style()
        self._load_icon()
    
    def _setup_style(self):
        self.setObjectName("SidebarBtn")
    
    def _load_icon(self):
        if self._icon_name:
            icon_path = osp.join('icons', self._icon_name)
            if osp.exists(icon_path):
                self.setIcon(QIcon(icon_path))
    
    def paintEvent(self, event: QPaintEvent):
        super().paintEvent(event)
        
        if self.isChecked():
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            
            # Draw active indicator (left border)
            painter.setBrush(QColor("#6366f1"))
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(2, 12, 4, 32, 2, 2)
            painter.end()


class SidebarSection(QFrame):
    """Collapsible Sidebar Section"""
    
    def __init__(self, title: str = "", parent=None):
        super().__init__(parent)
        self._title = title
        self._setup_ui()
    
    def _setup_ui(self):
        self.setFrameShape(QFrame.NoFrame)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(4, 8, 4, 8)
        self.layout.setSpacing(8)
        self.layout.setAlignment(Qt.AlignCenter)
    
    def add_button(self, button: SidebarButton):
        self.layout.addWidget(button, 0, Qt.AlignCenter)


class ModernSidebarNew(QWidget):
    """
    Slim Modern Sidebar (64px)
    """
    action_open = Signal()
    action_detect = Signal()
    action_ocr = Signal()
    action_translate = Signal()
    action_inpaint = Signal()
    action_batch = Signal()
    action_export = Signal()
    action_settings = Signal()
    
    page_list_toggled = Signal(bool)
    search_toggled = Signal(bool)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("ModernSidebar")
        self.setFixedWidth(64)
        
        self._setup_ui()
    
    def _setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 20, 0, 20)
        self.layout.setSpacing(10)
        self.layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        
        # Top Actions
        self.btn_open = SidebarButton("openbtn.svg", "Open Project", self)
        self.btn_open.clicked.connect(self.action_open.emit)
        
        self.showPageListLabel = SidebarButton("showpagelist.svg", "Files", self, checkable=True)
        self.showPageListLabel.clicked.connect(
            lambda: self.page_list_toggled.emit(self.showPageListLabel.isChecked())
        )
        
        self.layout.addWidget(self.btn_open)
        self.layout.addWidget(self.showPageListLabel)
        
        self._add_separator()
        
        # Tools
        self.btn_detect = SidebarButton("search.svg", "Detect", self)
        self.btn_detect.clicked.connect(self.action_detect.emit)
        
        self.btn_ocr = SidebarButton("bottombar_ocr.svg", "OCR", self)
        self.btn_ocr.clicked.connect(self.action_ocr.emit)
        
        self.btn_inpaint = SidebarButton("drawingtools_inpaint.svg", "Inpaint", self)
        self.btn_inpaint.clicked.connect(self.action_inpaint.emit)
        
        self.layout.addWidget(self.btn_detect)
        self.layout.addWidget(self.btn_ocr)
        self.layout.addWidget(self.btn_inpaint)
        
        self.layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        self._add_separator()
        
        # Bottom Actions
        self.btn_export = SidebarButton("save.svg", "Export", self)
        self.btn_export.clicked.connect(self.action_export.emit)
        
        self.configChecker = SidebarButton("leftbar_config.svg", "Settings", self, checkable=True)
        self.configChecker.clicked.connect(self.action_settings.emit)
        
        self.layout.addWidget(self.btn_export)
        self.layout.addWidget(self.configChecker)

        # Compatibility
        self.imgTransChecker = SidebarButton("", "", self, checkable=True)
        self.imgTransChecker.hide()
        self.imgTransChecker.setChecked(True)

    def _add_separator(self):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFixedWidth(32)
        line.setStyleSheet("background-color: rgba(255, 255, 255, 0.1); border: none; min-height: 1px;")
        self.layout.addWidget(line, 0, Qt.AlignCenter)

    def set_active_tool(self, tool_name: str):
        buttons = {
            'detect': self.btn_detect,
            'ocr': self.btn_ocr,
            'inpaint': self.btn_inpaint,
        }
        for name, btn in buttons.items():
            btn.setChecked(name == tool_name)

    def updateRecentProjList(self, path): pass

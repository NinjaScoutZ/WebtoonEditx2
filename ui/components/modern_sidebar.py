"""
Modern Sidebar Component
"""
from qtpy.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QToolButton, 
    QLabel, QSpacerItem, QSizePolicy, QFrame, QScrollArea
)
from qtpy.QtCore import Qt, Signal, QSize
from qtpy.QtGui import QIcon, QPainter, QColor, QPaintEvent
import os.path as osp


class SidebarButton(QToolButton):
    """Modern Sidebar Button with Icon and Text"""
    
    def __init__(self, icon_name: str, text: str, parent=None, checkable: bool = False):
        super().__init__(parent)
        self._icon_name = icon_name
        self._text = text
        self._badge_count = 0
        
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.setIconSize(QSize(28, 28))
        self.setCheckable(checkable)
        self.setAutoRaise(True)
        self.setFixedSize(72, 72)
        self.setCursor(Qt.PointingHandCursor)
        
        self._setup_style()
        self._load_icon()
    
    def _setup_style(self):
        self.setStyleSheet("""
            QToolButton {
                background-color: transparent;
                color: #94a3b8;
                border: none;
                border-radius: 12px;
                padding: 8px;
                font-size: 11px;
                font-weight: 500;
            }
            QToolButton:hover {
                background-color: #334155;
                color: #f1f5f9;
            }
            QToolButton:checked {
                background-color: #6366f1;
                color: white;
            }
            QToolButton:checked:hover {
                background-color: #4f46e5;
            }
        """)
    
    def _load_icon(self):
        if self._icon_name:
            icon_path = osp.join('icons', self._icon_name)
            if osp.exists(icon_path):
                self.setIcon(QIcon(icon_path))
        self.setText(self._text)
    
    def set_badge(self, count: int):
        """Set notification badge count"""
        self._badge_count = count
        self.update()
    
    def paintEvent(self, event: QPaintEvent):
        super().paintEvent(event)
        
        if self._badge_count > 0:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            
            # Draw badge circle
            painter.setBrush(QColor("#ef4444"))
            painter.setPen(Qt.NoPen)
            badge_rect = self.rect().adjusted(45, 8, -8, 45)
            painter.drawEllipse(badge_rect)
            
            # Draw badge text
            painter.setPen(QColor("white"))
            painter.setFont(self.font())
            text = str(min(self._badge_count, 99))
            painter.drawText(badge_rect, Qt.AlignCenter, text)
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
        self.layout.setContentsMargins(8, 8, 8, 8)
        self.layout.setSpacing(4)
        
        if self._title:
            self.title_label = QLabel(self._title)
            self.title_label.setStyleSheet("""
                color: #64748b;
                font-size: 10px;
                font-weight: 600;
                text-transform: uppercase;
                padding: 4px 8px;
            """)
            self.layout.addWidget(self.title_label)
    
    def add_button(self, button: SidebarButton):
        self.layout.addWidget(button)
    
    def add_widget(self, widget):
        self.layout.addWidget(widget)


class ModernSidebarNew(QWidget):
    """
    Modern Sidebar with Improved UX
    """
    # Action Signals
    action_open = Signal()
    action_detect = Signal()
    action_ocr = Signal()
    action_translate = Signal()
    action_inpaint = Signal()
    action_batch = Signal()
    action_export = Signal()
    action_settings = Signal()
    
    # Toggle Signals
    page_list_toggled = Signal(bool)
    search_toggled = Signal(bool)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("ModernSidebar")
        self.setFixedWidth(88)
        
        self._setup_ui()
        self._setup_sections()
    
    def _setup_ui(self):
        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(8, 16, 8, 16)
        self.main_layout.setSpacing(8)
        self.main_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        
        # Style
        self.setStyleSheet("""
            #ModernSidebar {
                background-color: #1e293b;
                border-right: 1px solid #334155;
            }
        """)
    
    def _setup_sections(self):
        # Top Section - Main Actions
        self.main_section = SidebarSection(parent=self)
        
        self.btn_open = SidebarButton("openbtn.svg", "Open", self)
        self.btn_open.clicked.connect(self.action_open.emit)
        
        self.showPageListLabel = SidebarButton("showpagelist.svg", "Files", self, checkable=True)
        self.showPageListLabel.clicked.connect(
            lambda: self.page_list_toggled.emit(self.showPageListLabel.isChecked())
        )
        
        self.globalSearchChecker = SidebarButton("search.svg", "Search", self, checkable=True)
        self.globalSearchChecker.clicked.connect(
            lambda: self.search_toggled.emit(self.globalSearchChecker.isChecked())
        )
        
        self.main_section.add_button(self.btn_open)
        self.main_section.add_button(self.showPageListLabel)
        self.main_section.add_button(self.globalSearchChecker)
        
        self.main_layout.addWidget(self.main_section)
        
        # Separator
        self._add_separator()
        
        # Process Section
        self.process_section = SidebarSection("Process", self)
        
        self.btn_detect = SidebarButton("search.svg", "Detect", self)
        self.btn_detect.clicked.connect(self.action_detect.emit)
        
        self.btn_ocr = SidebarButton("bottombar_ocr.svg", "OCR", self)
        self.btn_ocr.clicked.connect(self.action_ocr.emit)
        
        self.btn_inpaint = SidebarButton("drawingtools_inpaint.svg", "Inpaint", self)
        self.btn_inpaint.clicked.connect(self.action_inpaint.emit)
        
        self.btn_batch = SidebarButton("layers.svg", "Batch", self)
        self.btn_batch.clicked.connect(self.action_batch.emit)
        
        self.process_section.add_button(self.btn_detect)
        self.process_section.add_button(self.btn_ocr)
        self.process_section.add_button(self.btn_inpaint)
        self.process_section.add_button(self.btn_batch)
        
        self.main_layout.addWidget(self.process_section)
        
        # Spacer
        self.main_layout.addItem(
            QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )
        
        # Bottom Section
        self.bottom_section = SidebarSection(parent=self)
        
        self.btn_export = SidebarButton("save.svg", "Export", self)
        self.btn_export.clicked.connect(self.action_export.emit)
        
        self.configChecker = SidebarButton("leftbar_config.svg", "Settings", self, checkable=True)
        self.configChecker.clicked.connect(self.action_settings.emit)
        
        # Hidden imgTransChecker for compatibility
        self.imgTransChecker = SidebarButton("", "", self, checkable=True)
        self.imgTransChecker.hide()
        self.imgTransChecker.setChecked(True)
        
        self.bottom_section.add_button(self.btn_export)
        self.bottom_section.add_button(self.configChecker)
        
        self.main_layout.addWidget(self.bottom_section)
    
    def _add_separator(self):
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("color: #334155; max-height: 1px;")
        self.main_layout.addWidget(separator)
    
    # Compatibility Methods
    def updateRecentProjList(self, path):
        """Dummy method for compatibility"""
        pass
    
    def set_active_tool(self, tool_name: str):
        """Set active tool button"""
        buttons = {
            'detect': self.btn_detect,
            'ocr': self.btn_ocr,
            'inpaint': self.btn_inpaint,
            'batch': self.btn_batch,
        }
        for name, btn in buttons.items():
            btn.setChecked(name == tool_name)

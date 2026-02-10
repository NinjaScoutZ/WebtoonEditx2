"""
Modern MainWindow - Complete Rework with Dashboard and Animations
"""
import os.path as osp
import sys
from typing import List
from pathlib import Path

from qtpy.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
    QSplitter, QStackedWidget, QFileDialog, QMessageBox,
    QApplication, QShortcut, QLabel, QFrame, QGraphicsOpacityEffect
)
from qtpy.QtCore import Qt, Signal, QSize, QPropertyAnimation, QEasingCurve, QRect, Property
from qtpy.QtGui import QKeySequence, QIcon, QCloseEvent

# Utils
from utils.logger import logger as LOGGER
from utils import shared
from utils.config import ProgramConfig, pcfg, save_config

# UI Components
from .components import ModernSidebarNew, ModernCard
from .components.modern_titlebar import ModernTitleBar
from .components.modern_dashboard import ModernDashboard
from .themes import ModernTheme

# Legacy Components (wrapped)
from .canvas import Canvas
from .configpanel import ConfigPanel
from .scenetext_manager import SceneTextManager, TextPanel


class AnimatedPanel(QWidget):
    """A wrapper for panels that supports sliding animations"""
    def __init__(self, content_widget: QWidget, direction="left", parent=None):
        super().__init__(parent)
        self.direction = direction
        self.content = content_widget
        self.max_width = 300

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.content)

        self.setFixedWidth(0)
        self._is_expanded = False

        self.animation = QPropertyAnimation(self, b"minimumWidth")
        self.animation.setDuration(400)
        self.animation.setEasingCurve(QEasingCurve.OutExpo)

    def toggle(self):
        if self._is_expanded: self.collapse()
        else: self.expand()

    def expand(self):
        self.animation.setStartValue(self.width())
        self.animation.setEndValue(self.max_width)
        self.animation.start()
        self._is_expanded = True

    def collapse(self):
        self.animation.setStartValue(self.width())
        self.animation.setEndValue(0)
        self.animation.start()
        self._is_expanded = False


class ModernMainWindow(QMainWindow):
    """
    Modern MainWindow with Integrated Dashboard and Workspace
    """
    restart_signal = Signal()
    
    def __init__(self, app: QApplication, config: ProgramConfig, open_dir='', parent=None):
        super().__init__(parent)
        
        self.app = app
        self.config = config
        self.setWindowTitle("Modern Manga Translator")
        
        # Frameless Window
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)

        # Initialize theme
        self.theme = ModernTheme()
        self.apply_theme()
        
        # Setup window
        self.setMinimumSize(1200, 800)
        self.resize(1600, 900)
        
        # Setup central widget
        self.central_widget = QWidget()
        self.central_widget.setObjectName("CentralWidget")
        self.setCentralWidget(self.central_widget)
        
        self.main_v_layout = QVBoxLayout(self.central_widget)
        self.main_v_layout.setContentsMargins(0, 0, 0, 0)
        self.main_v_layout.setSpacing(0)

        # Title Bar
        self.title_bar = ModernTitleBar(self)
        self.main_v_layout.addWidget(self.title_bar)

        # Main Stack (Dashboard vs Workspace)
        self.main_stack = QStackedWidget()
        self.main_v_layout.addWidget(self.main_stack)

        # 1. Dashboard Page
        self.dashboard = ModernDashboard()
        self.dashboard.action_open.connect(self.on_open_project)
        self.dashboard.project_selected.connect(self.open_project)
        self.main_stack.addWidget(self.dashboard)

        # 2. Workspace Page
        self.workspace_page = QWidget()
        self.workspace_layout = QHBoxLayout(self.workspace_page)
        self.workspace_layout.setContentsMargins(0, 0, 0, 0)
        self.workspace_layout.setSpacing(0)
        self.main_stack.addWidget(self.workspace_page)

        self._setup_workspace_ui()
        self._setup_shortcuts()
        
        # Opacity effect for transitions
        self.opacity_effect = QGraphicsOpacityEffect(self.main_stack)
        self.main_stack.setGraphicsEffect(self.opacity_effect)
        self.fade_anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_anim.setDuration(500)

        # Load project if specified
        if open_dir and osp.exists(open_dir):
            self.open_project(open_dir)
        else:
            self.main_stack.setCurrentWidget(self.dashboard)
        
        self.show()
    
    def apply_theme(self):
        self.setStyleSheet(self.theme.get_stylesheet())
    
    def _setup_workspace_ui(self):
        """Setup workspace layout inside the stacked widget"""
        # Modern Sidebar
        self.sidebar = ModernSidebarNew(self)
        self.sidebar.action_open.connect(self.on_open_project)
        self.sidebar.action_detect.connect(self.on_detect)
        self.sidebar.action_ocr.connect(self.on_ocr)
        self.sidebar.action_inpaint.connect(self.on_inpaint)
        self.sidebar.page_list_toggled.connect(self.on_toggle_page_list)
        
        self.workspace_layout.addWidget(self.sidebar)
        
        # Left Panel (Page List) - Animated
        self.page_list_card = ModernCard("Pages", self)
        self.page_list_placeholder = QLabel("Project Page List Here")
        self.page_list_placeholder.setAlignment(Qt.AlignCenter)
        self.page_list_card.add_widget(self.page_list_placeholder)
        
        self.page_list_animated = AnimatedPanel(self.page_list_card, "left", self)
        self.workspace_layout.addWidget(self.page_list_animated)
        
        # Center Workspace
        self.workspace_container = QWidget()
        self.center_layout = QVBoxLayout(self.workspace_container)
        self.center_layout.setContentsMargins(12, 12, 12, 12)
        self.center_layout.setSpacing(12)
        
        self.canvas_card = ModernCard(parent=self)
        self.canvas_card.main_layout.setContentsMargins(0, 0, 0, 0)
        self.canvas = Canvas()
        self.canvas_card.add_widget(self.canvas.gv)
        
        self.center_layout.addWidget(self.canvas_card)
        self.workspace_layout.addWidget(self.workspace_container, 1)
        
        # Right Panel (Text Editor) - Animated
        self.text_panel_card = ModernCard("Editor", self)
        self.text_panel = TextPanel(self.app)
        self.text_panel_card.add_widget(self.text_panel)
        
        self.text_panel_animated = AnimatedPanel(self.text_panel_card, "right", self)
        self.text_panel_animated.max_width = 400
        self.workspace_layout.addWidget(self.text_panel_animated)
        
    def _setup_shortcuts(self):
        QShortcut(QKeySequence.Open, self, self.on_open_project)
        QShortcut(QKeySequence("Ctrl+B"), self, self.on_toggle_sidebar)
        QShortcut(QKeySequence("Ctrl+T"), self, self.on_toggle_text_panel)
        QShortcut(QKeySequence("Home"), self, self.go_home)
    
    def go_home(self):
        self._fade_to_widget(self.dashboard)

    def _fade_to_widget(self, widget):
        self.fade_anim.setStartValue(1.0)
        self.fade_anim.setEndValue(0.0)
        self.fade_anim.finished.connect(lambda: self._complete_fade(widget))
        self.fade_anim.start()

    def _complete_fade(self, widget):
        self.fade_anim.finished.disconnect()
        self.main_stack.setCurrentWidget(widget)
        self.fade_anim.setStartValue(0.0)
        self.fade_anim.setEndValue(1.0)
        self.fade_anim.start()

    def on_open_project(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Project Folder")
        if folder: self.open_project(folder)
    
    def open_project(self, path: str):
        self.title_bar.title_label.setText(f"Modern Manga Translator - {osp.basename(path)}")
        self._fade_to_widget(self.workspace_page)
        LOGGER.info(f"Loaded project: {path}")
    
    def on_detect(self): LOGGER.info("Detecting...")
    def on_ocr(self): LOGGER.info("OCR...")
    def on_inpaint(self): LOGGER.info("Inpainting...")
    
    def on_toggle_page_list(self, show: bool):
        if show: self.page_list_animated.expand()
        else: self.page_list_animated.collapse()

    def on_toggle_text_panel(self):
        self.text_panel_animated.toggle()
    
    def on_toggle_sidebar(self):
        self.sidebar.setVisible(not self.sidebar.isVisible())
    
    def closeEvent(self, event: QCloseEvent):
        save_config()
        event.accept()

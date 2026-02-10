"""
Modern MainWindow - Complete Rework
"""
import os.path as osp
import sys
from typing import List
from pathlib import Path

from qtpy.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
    QSplitter, QStackedWidget, QFileDialog, QMessageBox,
    QApplication, QShortcut, QLabel, QFrame
)
from qtpy.QtCore import Qt, Signal, QSize
from qtpy.QtGui import QKeySequence, QIcon, QCloseEvent

# Utils
from utils.logger import logger as LOGGER
from utils import shared
from utils.config import ProgramConfig, pcfg, save_config

# UI Components
from .components import ModernSidebarNew, ModernCard
from .components.modern_titlebar import ModernTitleBar
from .themes import ModernTheme

# Legacy Components (wrapped)
from .canvas import Canvas
from .configpanel import ConfigPanel
from .scenetext_manager import SceneTextManager, TextPanel


class ModernMainWindow(QMainWindow):
    """
    Modern MainWindow with Integrated Architecture and Frameless Experience
    """
    restart_signal = Signal()
    
    def __init__(self, app: QApplication, config: ProgramConfig, open_dir='', parent=None):
        super().__init__(parent)
        
        self.app = app
        self.config = config
        self.setWindowTitle("Modern Manga Translator")
        
        # Frameless Window
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setAttribute(Qt.WA_TranslucentBackground, False)

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

        # Main Body Layout
        self.body_layout = QHBoxLayout()
        self.body_layout.setContentsMargins(0, 0, 0, 0)
        self.body_layout.setSpacing(0)
        self.main_v_layout.addLayout(self.body_layout)

        # Initialize components
        self._setup_ui()
        self._setup_shortcuts()
        
        # Load project if specified
        if open_dir and osp.exists(open_dir):
            self.open_project(open_dir)
        
        self.show()
    
    def apply_theme(self):
        self.setStyleSheet(self.theme.get_stylesheet())
    
    def _setup_ui(self):
        """Setup main UI layout"""
        # Modern Sidebar
        self.sidebar = ModernSidebarNew(self)
        self.sidebar.action_open.connect(self.on_open_project)
        self.sidebar.action_detect.connect(self.on_detect)
        self.sidebar.action_ocr.connect(self.on_ocr)
        self.sidebar.action_inpaint.connect(self.on_inpaint)
        self.sidebar.page_list_toggled.connect(self.on_toggle_page_list)
        
        self.body_layout.addWidget(self.sidebar)
        
        # Workspace Splitter
        self.workspace_splitter = QSplitter(Qt.Horizontal)
        self.workspace_splitter.setHandleWidth(1)
        
        # Left Panel (Page List)
        self.page_list_card = ModernCard("Pages", self)
        self.page_list_placeholder = QLabel("Project Page List Here")
        self.page_list_placeholder.setAlignment(Qt.AlignCenter)
        self.page_list_placeholder.setStyleSheet("color: #64748b;")
        self.page_list_card.add_widget(self.page_list_placeholder)
        
        self.workspace_splitter.addWidget(self.page_list_card)
        self.page_list_card.hide()
        
        # Center Workspace
        self.workspace_container = QWidget()
        self.workspace_layout = QVBoxLayout(self.workspace_container)
        self.workspace_layout.setContentsMargins(12, 12, 12, 12)
        self.workspace_layout.setSpacing(12)
        
        self.canvas_card = ModernCard(parent=self)
        self.canvas_card.main_layout.setContentsMargins(0, 0, 0, 0)
        self.canvas = Canvas()
        self.canvas_card.add_widget(self.canvas.gv)
        
        self.workspace_layout.addWidget(self.canvas_card)
        self.workspace_splitter.addWidget(self.workspace_container)
        self.workspace_splitter.setStretchFactor(1, 1)
        
        # Right Panel (Text Editor)
        self.text_panel_card = ModernCard("Editor", self)
        self.text_panel = TextPanel(self.app)
        self.text_panel_card.add_widget(self.text_panel)
        
        self.workspace_splitter.addWidget(self.text_panel_card)
        self.workspace_splitter.setStretchFactor(2, 0)
        
        self.body_layout.addWidget(self.workspace_splitter)
        
    def _setup_shortcuts(self):
        QShortcut(QKeySequence.Open, self, self.on_open_project)
        QShortcut(QKeySequence("Ctrl+B"), self, self.on_toggle_sidebar)
    
    def on_open_project(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Project Folder")
        if folder: self.open_project(folder)
    
    def open_project(self, path: str):
        self.title_bar.title_label.setText(f"Modern Manga Translator - {osp.basename(path)}")
    
    def on_detect(self): LOGGER.info("Detecting...")
    def on_ocr(self): LOGGER.info("OCR...")
    def on_inpaint(self): LOGGER.info("Inpainting...")
    
    def on_toggle_page_list(self, show: bool):
        self.page_list_card.setVisible(show)
    
    def on_toggle_sidebar(self):
        self.sidebar.setVisible(not self.sidebar.isVisible())
    
    def closeEvent(self, event: QCloseEvent):
        save_config()
        event.accept()

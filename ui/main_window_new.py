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
    QApplication, QShortcut, QLabel
)
from qtpy.QtCore import Qt, Signal, QSize
from qtpy.QtGui import QKeySequence, QIcon, QCloseEvent

# Utils
from utils.logger import logger as LOGGER
from utils import shared
from utils.config import ProgramConfig, pcfg, save_config

# UI Components
from .components import ModernSidebarNew
from .themes import ModernTheme

# Legacy Components (wrapped)
from .canvas import Canvas
from .configpanel import ConfigPanel
from .scenetext_manager import SceneTextManager, TextPanel
from .module_manager import ModuleManager
from .global_search_widget import GlobalSearchWidget
from .io_thread import ImgSaveThread, ImportDocThread, ExportDocThread


class ModernMainWindow(QMainWindow):
    """
    Modern MainWindow with Improved Architecture
    """
    restart_signal = Signal()
    
    def __init__(self, app: QApplication, config: ProgramConfig, open_dir='', parent=None):
        super().__init__(parent)
        
        self.app = app
        self.config = config
        self.setWindowTitle("Modern Manga Translator")
        
        # Initialize theme
        self.theme = ModernTheme()
        self.apply_theme()
        
        # Setup window
        self.setMinimumSize(1200, 800)
        self.resize(1600, 900)
        
        # Setup central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Initialize components
        self._setup_threads()
        self._setup_ui()
        self._setup_shortcuts()
        
        # Load project if specified
        if open_dir and osp.exists(open_dir):
            self.open_project(open_dir)
        elif pcfg.open_recent_on_startup and pcfg.recent_proj_list:
            recent = pcfg.recent_proj_list[0]
            if osp.exists(recent):
                self.open_project(recent)
        
        self.show()
    
    def apply_theme(self):
        """Apply modern theme stylesheet"""
        self.setStyleSheet(self.theme.get_stylesheet())
    
    def _setup_threads(self):
        """Setup background threads"""
        self.imsave_thread = ImgSaveThread()
        self.export_doc_thread = ExportDocThread()
        self.import_doc_thread = ImportDocThread(self)
    
    def _setup_ui(self):
        """Setup main UI layout"""
        # Main horizontal layout
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Modern Sidebar
        self.sidebar = ModernSidebarNew(self)
        self.sidebar.action_open.connect(self.on_open_project)
        self.sidebar.action_detect.connect(self.on_detect)
        self.sidebar.action_ocr.connect(self.on_ocr)
        self.sidebar.action_inpaint.connect(self.on_inpaint)
        self.sidebar.action_batch.connect(self.on_batch)
        self.sidebar.action_export.connect(self.on_export)
        self.sidebar.action_settings.connect(self.on_settings)
        self.sidebar.page_list_toggled.connect(self.on_toggle_page_list)
        self.sidebar.search_toggled.connect(self.on_toggle_search)
        
        self.main_layout.addWidget(self.sidebar)
        
        # Content area with splitter
        self.content_splitter = QSplitter(Qt.Horizontal)
        
        # Left panel (Page List / Search)
        self.left_panel = QStackedWidget()
        self.left_panel.setMinimumWidth(200)
        self.left_panel.setMaximumWidth(350)
        
        # Page list placeholder
        self.page_list_widget = QWidget()
        self.page_list_layout = QVBoxLayout(self.page_list_widget)
        self.page_list_layout.addWidget(QLabel("Page List"))
        self.left_panel.addWidget(self.page_list_widget)
        
        # Search placeholder
        self.search_widget = QWidget()
        self.search_layout = QVBoxLayout(self.search_widget)
        self.search_layout.addWidget(QLabel("Global Search"))
        self.left_panel.addWidget(self.search_widget)
        
        self.content_splitter.addWidget(self.left_panel)
        
        # Center area (Canvas + Config)
        self.center_stack = QStackedWidget()
        
        # Canvas view
        self.canvas_container = QWidget()
        self.canvas_layout = QVBoxLayout(self.canvas_container)
        self.canvas_layout.setContentsMargins(0, 0, 0, 0)
        
        # Initialize canvas
        self.canvas = Canvas()
        self.canvas_layout.addWidget(self.canvas.gv)
        
        self.center_stack.addWidget(self.canvas_container)
        
        # Config panel
        self.config_panel = ConfigPanel(self)
        self.center_stack.addWidget(self.config_panel)
        
        self.content_splitter.addWidget(self.center_stack)
        self.content_splitter.setStretchFactor(1, 1)
        
        # Right panel (Text Editor)
        self.right_panel = TextPanel(self.app)
        self.right_panel.setMinimumWidth(300)
        self.right_panel.setMaximumWidth(450)
        
        self.content_splitter.addWidget(self.right_panel)
        self.content_splitter.setStretchFactor(2, 0)
        
        self.main_layout.addWidget(self.content_splitter, 1)
        
        # Set initial state
        self.left_panel.hide()
    
    def _setup_shortcuts(self):
        """Setup keyboard shortcuts"""
        # File operations
        QShortcut(QKeySequence.Open, self, self.on_open_project)
        QShortcut(QKeySequence.Save, self, self.on_save)
        
        # View toggles
        QShortcut(QKeySequence("Ctrl+T"), self, self.on_toggle_text_panel)
        QShortcut(QKeySequence("Ctrl+B"), self, self.on_toggle_sidebar)
        
        # Tools
        QShortcut(QKeySequence("D"), self, self.on_detect)
        QShortcut(QKeySequence("O"), self, self.on_ocr)
        QShortcut(QKeySequence("I"), self, self.on_inpaint)
    
    # ===== Action Handlers =====
    
    def on_open_project(self):
        """Open project folder"""
        folder = QFileDialog.getExistingDirectory(
            self, 
            self.tr("Select Project Folder"),
            ""
        )
        if folder:
            self.open_project(folder)
    
    def open_project(self, path: str):
        """Open project at path"""
        LOGGER.info(f"Opening project: {path}")
        # TODO: Implement project loading
        self.setWindowTitle(f"Modern Manga Translator - {osp.basename(path)}")
    
    def on_save(self):
        """Save project"""
        LOGGER.info("Saving project...")
        save_config()
    
    def on_detect(self):
        """Run text detection"""
        LOGGER.info("Running text detection...")
        self.sidebar.set_active_tool('detect')
        self.show_config_panel()
        self.config_panel.focusOnDetect()
    
    def on_ocr(self):
        """Run OCR"""
        LOGGER.info("Running OCR...")
        self.sidebar.set_active_tool('ocr')
        self.show_config_panel()
        self.config_panel.focusOnOCR()
    
    def on_inpaint(self):
        """Run inpainting"""
        LOGGER.info("Running inpainting...")
        self.sidebar.set_active_tool('inpaint')
        self.show_config_panel()
        self.config_panel.focusOnInpaint()
    
    def on_batch(self):
        """Open batch processing"""
        LOGGER.info("Opening batch processing...")
        QMessageBox.information(self, "Batch", "Batch processing dialog here")
    
    def on_export(self):
        """Export project"""
        LOGGER.info("Exporting project...")
    
    def on_settings(self):
        """Toggle settings panel"""
        self.show_config_panel()
    
    def on_toggle_page_list(self, show: bool):
        """Toggle page list visibility"""
        if show:
            self.left_panel.show()
            self.left_panel.setCurrentWidget(self.page_list_widget)
        else:
            if self.left_panel.currentWidget() == self.page_list_widget:
                self.left_panel.hide()
    
    def on_toggle_search(self, show: bool):
        """Toggle search panel visibility"""
        if show:
            self.left_panel.show()
            self.left_panel.setCurrentWidget(self.search_widget)
        else:
            if self.left_panel.currentWidget() == self.search_widget:
                self.left_panel.hide()
    
    def on_toggle_text_panel(self):
        """Toggle right text panel"""
        self.right_panel.setVisible(not self.right_panel.isVisible())
    
    def on_toggle_sidebar(self):
        """Toggle left sidebar"""
        self.sidebar.setVisible(not self.sidebar.isVisible())
    
    def show_config_panel(self):
        """Show configuration panel"""
        self.center_stack.setCurrentWidget(self.config_panel)
    
    def show_canvas(self):
        """Show canvas view"""
        self.center_stack.setCurrentWidget(self.canvas_container)
    
    def closeEvent(self, event: QCloseEvent):
        """Handle window close"""
        save_config()
        event.accept()

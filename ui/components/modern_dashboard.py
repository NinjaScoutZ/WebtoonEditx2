"""
Modern Dashboard Component - Stunning Welcome Screen
"""
from qtpy.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QScrollArea, QGridLayout, QFrame
)
from qtpy.QtCore import Qt, Signal, QSize
from qtpy.QtGui import QIcon, QPixmap, QFont

from .modern_button import ModernButton
from .modern_card import ModernCard


class ProjectCard(ModernCard):
    """A card representing a recent project"""
    clicked = Signal(str)

    def __init__(self, name: str, path: str, parent=None):
        super().__init__(parent=parent)
        self.path = path
        self.setFixedSize(240, 180)
        self.setCursor(Qt.PointingHandCursor)

        # Thumbnail placeholder
        self.thumb = QLabel()
        self.thumb.setFixedSize(208, 100)
        self.thumb.setStyleSheet("background-color: #020617; border-radius: 8px;")
        self.thumb.setAlignment(Qt.AlignCenter)
        self.thumb.setText("No Preview")

        # Title
        self.title = QLabel(name)
        self.title.setStyleSheet("font-weight: 700; font-size: 13px;")

        # Path
        self.path_lbl = QLabel(path)
        self.path_lbl.setObjectName("SubText")
        self.path_lbl.setWordWrap(True)
        self.path_lbl.setMaximumHeight(40)

        self.add_widget(self.thumb)
        self.add_widget(self.title)
        self.add_widget(self.path_lbl)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.path)
        super().mousePressEvent(event)


class ModernDashboard(QWidget):
    """
    Minimalist and Beautiful Dashboard for start screen
    """
    action_open = Signal()
    action_new = Signal()
    project_selected = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(60, 60, 60, 60)
        self.main_layout.setSpacing(40)

        # Header Section
        self.header = QVBoxLayout()
        self.welcome_lbl = QLabel("Welcome back")
        self.welcome_lbl.setStyleSheet("font-size: 32px; font-weight: 800; color: #f8fafc;")

        self.subtitle = QLabel("Start a new project or continue where you left off.")
        self.subtitle.setObjectName("SubText")
        self.subtitle.setStyleSheet("font-size: 16px;")

        self.header.addWidget(self.welcome_lbl)
        self.header.addWidget(self.subtitle)
        self.main_layout.addLayout(self.header)

        # Quick Actions Section
        self.actions_layout = QHBoxLayout()
        self.actions_layout.setSpacing(16)

        self.btn_new = ModernButton("Create New Project", primary=True)
        self.btn_new.clicked.connect(self.action_new.emit)

        self.btn_open = ModernButton("Open Existing Folder")
        self.btn_open.clicked.connect(self.action_open.emit)

        self.actions_layout.addWidget(self.btn_new)
        self.actions_layout.addWidget(self.btn_open)
        self.actions_layout.addStretch()
        self.main_layout.addLayout(self.actions_layout)

        # Recent Projects Section
        self.recent_lbl = QLabel("Recent Projects")
        self.recent_lbl.setStyleSheet("font-size: 18px; font-weight: 700;")
        self.main_layout.addWidget(self.recent_lbl)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.NoFrame)
        self.scroll.setStyleSheet("background: transparent;")

        self.projects_container = QWidget()
        self.projects_grid = QGridLayout(self.projects_container)
        self.projects_grid.setContentsMargins(0, 0, 0, 0)
        self.projects_grid.setSpacing(24)

        # Placeholder projects for visual demonstration
        self.add_project("Manga Chapter 01", "/path/to/manga/ch01")
        self.add_project("Webtoon Project", "/docs/webtoon/my_project")

        self.scroll.setWidget(self.projects_container)
        self.main_layout.addWidget(self.scroll, 1)

    def add_project(self, name, path):
        count = self.projects_grid.count()
        row = count // 4
        col = count % 4
        card = ProjectCard(name, path)
        card.clicked.connect(self.project_selected.emit)
        self.projects_grid.addWidget(card, row, col)

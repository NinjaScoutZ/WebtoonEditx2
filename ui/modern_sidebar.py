"""
Modern Sidebar for ModernMangaTranslator.
Vertical sidebar with icon buttons, animated hover effects, and active indicators.
Compatible with legacy leftBar interface (configChecker, imgTransChecker, etc.).
"""

from qtpy.QtWidgets import (
    QWidget, QVBoxLayout, QToolButton, QLabel, QSpacerItem, QSizePolicy,
    QGraphicsDropShadowEffect, QFrame
)
from qtpy.QtCore import Qt, QSize, Signal, QPropertyAnimation, QEasingCurve, QTimer
from qtpy.QtGui import QIcon, QColor, QPainter, QLinearGradient, QPen
import os.path as osp


ICON_DIR = 'icons'


class SidebarButton(QToolButton):
    """Modern sidebar button with hover glow animation."""

    def __init__(self, icon_name: str, tooltip: str, parent=None, checkable=False):
        super().__init__(parent)
        self.setToolTip(tooltip)
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.setIconSize(QSize(24, 24))
        if icon_name:
            icon_path = osp.join(ICON_DIR, icon_name)
            if osp.exists(icon_path):
                self.setIcon(QIcon(icon_path))
        self.setCheckable(checkable)
        self.setAutoRaise(True)
        self.setFixedSize(48, 48)
        self.setObjectName("SidebarBtn")
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # Glow effect
        self._glow = QGraphicsDropShadowEffect(self)
        self._glow.setBlurRadius(0)
        self._glow.setColor(QColor(139, 92, 246, 120))
        self._glow.setOffset(0, 0)
        self.setGraphicsEffect(self._glow)

    def enterEvent(self, event):
        anim = QPropertyAnimation(self._glow, b"blurRadius", self)
        anim.setDuration(200)
        anim.setStartValue(0)
        anim.setEndValue(20)
        anim.setEasingCurve(QEasingCurve.Type.OutQuad)
        anim.start(QPropertyAnimation.DeletionPolicy.DeleteWhenStopped)
        super().enterEvent(event)

    def leaveEvent(self, event):
        anim = QPropertyAnimation(self._glow, b"blurRadius", self)
        anim.setDuration(200)
        anim.setStartValue(20)
        anim.setEndValue(0)
        anim.setEasingCurve(QEasingCurve.Type.InQuad)
        anim.start(QPropertyAnimation.DeletionPolicy.DeleteWhenStopped)
        super().leaveEvent(event)


class SidebarSeparator(QFrame):
    """Thin line separator for sidebar sections."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.HLine)
        self.setFixedHeight(1)
        self.setStyleSheet("background-color: rgba(255, 255, 255, 0.08); border: none;")


class ModernSidebar(QWidget):
    """
    Modern vertical sidebar with icon-based navigation.
    Provides signals for all actions and compat attributes for legacy code.
    """

    # Action signals
    action_open = Signal()
    action_detect = Signal()
    action_ocr = Signal()
    action_inpaint = Signal()
    action_batch = Signal()
    action_export = Signal()
    action_settings = Signal()

    # State toggle signals
    page_list_toggled = Signal(bool)
    search_toggled = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(64)
        self.setObjectName("ModernSidebar")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 16, 8, 16)
        layout.setSpacing(6)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # === Top Section: Navigation ===
        self.btn_open = SidebarButton("openbtn.svg", "Open Project (Ctrl+O)", self)
        self.btn_open.clicked.connect(self.action_open.emit)

        # Toggle buttons (checkable)
        self.showPageListLabel = SidebarButton("showpagelist.svg", "File List", self, checkable=True)
        self.showPageListLabel.clicked.connect(
            lambda: self.page_list_toggled.emit(self.showPageListLabel.isChecked())
        )

        self.globalSearchChecker = SidebarButton("search.svg", "Global Search (Ctrl+G)", self, checkable=True)
        self.globalSearchChecker.clicked.connect(
            lambda: self.search_toggled.emit(self.globalSearchChecker.isChecked())
        )

        layout.addWidget(self.btn_open, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.showPageListLabel, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.globalSearchChecker, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(SidebarSeparator(self))

        # === Middle Section: Actions ===
        self.btn_detect = SidebarButton("search.svg", "Detect Text", self)
        self.btn_detect.clicked.connect(self.action_detect.emit)

        self.btn_ocr = SidebarButton("bottombar_ocr.svg", "Run OCR", self)
        self.btn_ocr.clicked.connect(self.action_ocr.emit)

        self.btn_inpaint = SidebarButton("drawingtools_inpaint.svg", "Inpaint", self)
        self.btn_inpaint.clicked.connect(self.action_inpaint.emit)

        self.btn_batch = SidebarButton("layers.svg", "Batch Process", self)
        self.btn_batch.clicked.connect(self.action_batch.emit)

        layout.addWidget(self.btn_detect, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.btn_ocr, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.btn_inpaint, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.btn_batch, alignment=Qt.AlignmentFlag.AlignCenter)

        # === Spacer ===
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        layout.addWidget(SidebarSeparator(self))

        # === Bottom Section: Utility ===
        self.btn_export = SidebarButton("save.svg", "Export", self)
        self.btn_export.clicked.connect(self.action_export.emit)

        self.configChecker = SidebarButton("leftbar_config.svg", "Settings", self, checkable=True)
        self.configChecker.clicked.connect(self.action_settings.emit)

        layout.addWidget(self.btn_export, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.configChecker, alignment=Qt.AlignmentFlag.AlignCenter)

        # === Hidden compat widgets ===
        self.imgTransChecker = SidebarButton("", "", self, checkable=True)
        self.imgTransChecker.hide()
        self.imgTransChecker.setChecked(True)

    def updateRecentProjList(self, path):
        """Compat stub for legacy leftBar.updateRecentProjList()."""
        pass

    def paintEvent(self, event):
        """Draw subtle gradient background."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Darker slate gradient
        grad = QLinearGradient(0, 0, 0, self.height())
        grad.setColorAt(0, QColor(15, 23, 42, 255))   # Slate-900 opaque
        grad.setColorAt(1, QColor(2, 6, 23, 255))     # Slate-950 opaque
        painter.fillRect(self.rect(), grad)

        # Right border line
        pen = QPen(QColor(255, 255, 255, 25))
        pen.setWidth(1)
        painter.setPen(pen)
        painter.drawLine(self.width() - 1, 0, self.width() - 1, self.height())

        painter.end()

"""
Floating Toolbar for canvas tools.
Sits at the top-center of the canvas area with glassmorphism styling.
"""

from qtpy.QtWidgets import (
    QFrame, QHBoxLayout, QToolButton, QSlider, QLabel,
    QGraphicsDropShadowEffect
)
from qtpy.QtCore import Qt, QSize, Signal, QPropertyAnimation, QEasingCurve
from qtpy.QtGui import QIcon, QColor, QPainter, QLinearGradient, QPen
import os.path as osp

ICON_DIR = 'icons'


class ToolbarButton(QToolButton):
    """Toolbar tool button with hover glow."""

    def __init__(self, icon_name: str, tooltip: str, parent=None, checkable=True):
        super().__init__(parent)
        self.setToolTip(tooltip)
        self.setIconSize(QSize(20, 20))
        if icon_name:
            icon_path = osp.join(ICON_DIR, icon_name)
            if osp.exists(icon_path):
                self.setIcon(QIcon(icon_path))
        self.setCheckable(checkable)
        self.setAutoRaise(True)
        self.setFixedSize(36, 36)
        self.setObjectName("ToolbarBtn")
        self.setCursor(Qt.CursorShape.PointingHandCursor)


class ActionButton(QToolButton):
    """Special action button with gradient styling (e.g., Inpaint)."""

    def __init__(self, text: str, tooltip: str, parent=None):
        super().__init__(parent)
        self.setText(text)
        self.setToolTip(tooltip)
        self.setFixedHeight(32)
        self.setMinimumWidth(80)
        self.setObjectName("InpaintActionBtn")
        self.setCursor(Qt.CursorShape.PointingHandCursor)


class FloatingToolbar(QFrame):
    """
    Floating toolbar with tool buttons, size slider, and action buttons.
    Emits signals when tools are selected.
    """

    tool_changed = Signal(str)  # 'select', 'rect', 'brush', 'eraser'
    action_inpaint = Signal()
    action_clear = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("FloatingToolbar")
        self.setFixedHeight(52)

        # Drop shadow
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 100))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(6)

        # Tool buttons (exclusive group)
        self.btn_select = ToolbarButton("cursor.svg", "Select (V)", self)
        self.btn_rect = ToolbarButton("rect.svg", "Rectangle (M)", self)
        self.btn_brush = ToolbarButton("brush.svg", "Brush (B)", self)
        self.btn_eraser = ToolbarButton("eraser.svg", "Eraser (E)", self)

        self.btn_select.setChecked(True)
        self._current_tool = 'select'

        # Exclusive toggle behavior
        self._tool_buttons = [self.btn_select, self.btn_rect, self.btn_brush, self.btn_eraser]
        for btn in self._tool_buttons:
            btn.clicked.connect(self._on_tool_clicked)

        layout.addWidget(self.btn_select)
        layout.addWidget(self.btn_rect)
        layout.addWidget(self.btn_brush)
        layout.addWidget(self.btn_eraser)

        # Separator
        sep = QFrame(self)
        sep.setFrameShape(QFrame.Shape.VLine)
        sep.setFixedHeight(24)
        sep.setStyleSheet("color: rgba(255,255,255,0.15); border: none; background: rgba(255,255,255,0.1); max-width: 1px;")
        layout.addWidget(sep)

        # Size slider
        size_label = QLabel("Size:", self)
        size_label.setStyleSheet("color: rgba(248,250,252,0.6); font-size: 11px; border: none; background: transparent;")
        self.size_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.size_slider.setRange(1, 100)
        self.size_slider.setValue(20)
        self.size_slider.setFixedWidth(80)
        self.size_slider.setStyleSheet("""
            QSlider::groove:horizontal { background: rgba(255,255,255,0.1); height: 4px; border-radius: 2px; }
            QSlider::handle:horizontal { background: #8b5cf6; width: 14px; height: 14px; margin: -5px 0; border-radius: 7px; }
            QSlider::sub-page:horizontal { background: #8b5cf6; border-radius: 2px; }
        """)

        layout.addWidget(size_label)
        layout.addWidget(self.size_slider)

        # Separator 2
        sep2 = QFrame(self)
        sep2.setFrameShape(QFrame.Shape.VLine)
        sep2.setFixedHeight(24)
        sep2.setStyleSheet("color: rgba(255,255,255,0.15); border: none; background: rgba(255,255,255,0.1); max-width: 1px;")
        layout.addWidget(sep2)

        # Action buttons
        self.btn_clear = ToolbarButton("trash.svg", "Clear Masks", self, checkable=False)
        self.btn_clear.clicked.connect(self.action_clear.emit)

        self.btn_inpaint = ActionButton("✨ Inpaint", "Run Inpaint on Mask", self)
        self.btn_inpaint.clicked.connect(self.action_inpaint.emit)

        layout.addWidget(self.btn_clear)
        layout.addWidget(self.btn_inpaint)

        self.adjustSize()

    def _on_tool_clicked(self):
        sender = self.sender()
        tool_map = {
            self.btn_select: 'select',
            self.btn_rect: 'rect',
            self.btn_brush: 'brush',
            self.btn_eraser: 'eraser'
        }

        # Exclusive: uncheck all others
        for btn in self._tool_buttons:
            if btn != sender:
                btn.setChecked(False)
        sender.setChecked(True)

        tool = tool_map.get(sender, 'select')
        if tool != self._current_tool:
            self._current_tool = tool
            self.tool_changed.emit(tool)

    def paintEvent(self, event):
        """Draw glassmorphism background."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Glass background
        rect = self.rect()
        painter.setBrush(QColor(30, 41, 59, 220))
        painter.setPen(QPen(QColor(255, 255, 255, 20), 1))
        painter.drawRoundedRect(rect.adjusted(0, 0, -1, -1), 16, 16)

        painter.end()

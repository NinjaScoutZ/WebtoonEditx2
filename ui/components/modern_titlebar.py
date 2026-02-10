"""
Modern Title Bar Component
"""
from qtpy.QtWidgets import QWidget, QHBoxLayout, QLabel, QToolButton, QApplication
from qtpy.QtCore import Qt, QPoint, QSize
from qtpy.QtGui import QIcon, QColor


class ModernTitleBar(QWidget):
    """Custom Title Bar for Frameless Window"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(48)
        self._setup_ui()

    def _setup_ui(self):
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(16, 0, 8, 0)
        self.layout.setSpacing(8)

        # Logo and Title
        self.title_label = QLabel("Modern Manga Translator")
        self.title_label.setStyleSheet("font-weight: 700; color: #f8fafc; font-size: 14px;")
        self.layout.addWidget(self.title_label)

        self.layout.addStretch()

        # Window Controls
        self.btn_min = self._create_control_btn("minimize.svg", self.window().showMinimized)
        self.btn_max = self._create_control_btn("maximize.svg", self._toggle_maximized)
        self.btn_close = self._create_control_btn("close.svg", self.window().close)
        self.btn_close.setStyleSheet("QToolButton:hover { background-color: #ef4444; }")

        self.layout.addWidget(self.btn_min)
        self.layout.addWidget(self.btn_max)
        self.layout.addWidget(self.btn_close)

    def _create_control_btn(self, icon, callback):
        btn = QToolButton(self)
        btn.setFixedSize(40, 40)
        btn.setAutoRaise(True)
        btn.clicked.connect(callback)
        btn.setStyleSheet("""
            QToolButton {
                border-radius: 8px;
                background-color: transparent;
                border: none;
            }
            QToolButton:hover {
                background-color: rgba(255, 255, 255, 0.08);
            }
        """)
        return btn

    def _toggle_maximized(self):
        if self.window().isMaximized():
            self.window().showNormal()
        else:
            self.window().showMaximized()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPos() - self.window().frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.window().move(event.globalPos() - self._drag_pos)
            event.accept()

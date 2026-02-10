"""
Loading overlay and spinner widgets for ModernMangaTranslator.
Provides visual feedback during long-running operations (Detect, OCR, Inpaint, Export).
"""
import math
from qtpy.QtWidgets import QWidget, QVBoxLayout, QLabel, QGraphicsOpacityEffect
from qtpy.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, Property, QRect
from qtpy.QtGui import QPainter, QColor, QPen, QConicalGradient, QFont


class LoadingSpinner(QWidget):
    """Custom animated spinning indicator."""

    def __init__(self, parent=None, size=64, line_width=4):
        super().__init__(parent)
        self.setFixedSize(size, size)
        self._size = size
        self._line_width = line_width
        self._angle = 0
        self._arc_length = 90  # degrees

        # Colors
        self._color_primary = QColor("#8B5CF6")  # Purple
        self._color_secondary = QColor("#3B82F6")  # Blue
        self._color_trail = QColor(255, 255, 255, 30)

        # Animation timer
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._rotate)
        self._speed = 12  # ms per frame

    def start(self):
        self._timer.start(self._speed)

    def stop(self):
        self._timer.stop()

    def _rotate(self):
        self._angle = (self._angle + 4) % 360
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = QRect(
            self._line_width,
            self._line_width,
            self._size - 2 * self._line_width,
            self._size - 2 * self._line_width
        )

        # Trail circle
        trail_pen = QPen(self._color_trail)
        trail_pen.setWidth(self._line_width)
        trail_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(trail_pen)
        painter.drawArc(rect, 0, 360 * 16)

        # Spinning arc with gradient
        gradient = QConicalGradient(
            self._size / 2, self._size / 2,
            -self._angle
        )
        gradient.setColorAt(0, self._color_primary)
        gradient.setColorAt(0.5, self._color_secondary)
        gradient.setColorAt(1, QColor(self._color_primary.red(), self._color_primary.green(), self._color_primary.blue(), 0))

        arc_pen = QPen()
        arc_pen.setWidth(self._line_width)
        arc_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        arc_pen.setBrush(gradient)
        painter.setPen(arc_pen)

        start_angle = int(self._angle * 16)
        span_angle = int(self._arc_length * 16)
        painter.drawArc(rect, start_angle, span_angle)

        painter.end()


class LoadingOverlay(QWidget):
    """
    Semi-transparent overlay that covers parent widget.
    Shows a spinner + status text during long operations.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
        self.setStyleSheet("background: transparent;")
        self.hide()

        # Main layout
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Spinner
        self.spinner = LoadingSpinner(self, size=72, line_width=5)
        layout.addWidget(self.spinner, alignment=Qt.AlignmentFlag.AlignCenter)

        # Status label
        self.status_label = QLabel("Loading...", self)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                color: #F8FAFC;
                font-size: 15px;
                font-weight: 600;
                font-family: 'Segoe UI', 'Inter', sans-serif;
                background: transparent;
                margin-top: 16px;
                border: none;
            }
        """)
        layout.addWidget(self.status_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Sub-status
        self.sub_label = QLabel("", self)
        self.sub_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sub_label.setStyleSheet("""
            QLabel {
                color: rgba(248, 250, 252, 0.6);
                font-size: 12px;
                font-family: 'Segoe UI', 'Inter', sans-serif;
                background: transparent;
                border: none;
            }
        """)
        layout.addWidget(self.sub_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Fade animation
        self._opacity_effect = QGraphicsOpacityEffect(self)
        self._opacity_effect.setOpacity(0.0)
        self.setGraphicsEffect(self._opacity_effect)

        self._fade_anim = QPropertyAnimation(self._opacity_effect, b"opacity")
        self._fade_anim.setDuration(250)
        self._fade_anim.setEasingCurve(QEasingCurve.Type.InOutQuad)

    def showLoading(self, message="Processing...", sub_message=""):
        """Show the overlay with fade-in animation."""
        self.status_label.setText(message)
        self.sub_label.setText(sub_message)
        self.sub_label.setVisible(bool(sub_message))

        # Resize to cover parent
        if self.parent():
            self.setGeometry(self.parent().rect())

        self.show()
        self.raise_()
        self.spinner.start()

        self._fade_anim.stop()
        self._fade_anim.setStartValue(0.0)
        self._fade_anim.setEndValue(1.0)
        self._fade_anim.start()

    def hideLoading(self):
        """Hide the overlay with fade-out animation."""
        self._fade_anim.stop()
        self._fade_anim.setStartValue(1.0)
        self._fade_anim.setEndValue(0.0)
        self._fade_anim.finished.connect(self._on_fade_out_finished)
        self._fade_anim.start()

    def _on_fade_out_finished(self):
        self._fade_anim.finished.disconnect(self._on_fade_out_finished)
        self.spinner.stop()
        self.hide()

    def updateStatus(self, message, sub_message=""):
        """Update the status text while loading."""
        self.status_label.setText(message)
        self.sub_label.setText(sub_message)
        self.sub_label.setVisible(bool(sub_message))

    def paintEvent(self, event):
        """Draw semi-transparent dark backdrop."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor(2, 6, 23, 200))  # Slate-950 with alpha
        painter.end()

    def resizeEvent(self, event):
        super().resizeEvent(event)

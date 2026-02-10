"""
Modern Slider Component
"""
from qtpy.QtWidgets import QWidget, QHBoxLayout, QLabel, QSlider
from qtpy.QtCore import Qt, Signal


class ModernSlider(QWidget):
    """Modern Slider with Value Label"""
    
    value_changed = Signal(int)
    
    def __init__(self, label: str = "", min_val: int = 0, max_val: int = 100, 
                 default: int = 50, parent=None):
        super().__init__(parent)
        
        self._label_text = label
        self._min = min_val
        self._max = max_val
        
        self._setup_ui()
        self.slider.setValue(default)
        self._update_label(default)
    
    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        
        # Label
        if self._label_text:
            self.label = QLabel(self._label_text)
            self.label.setStyleSheet("color: #cbd5e1; font-size: 12px;")
            layout.addWidget(self.label)
        
        # Slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(self._min)
        self.slider.setMaximum(self._max)
        self.slider.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 6px;
                background: #334155;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: #6366f1;
                width: 16px;
                height: 16px;
                margin: -5px 0;
                border-radius: 8px;
            }
            QSlider::sub-page:horizontal {
                background: #6366f1;
                border-radius: 3px;
            }
        """)
        self.slider.valueChanged.connect(self._on_value_changed)
        layout.addWidget(self.slider, 1)
        
        # Value Label
        self.value_label = QLabel()
        self.value_label.setStyleSheet("color: #f8fafc; font-size: 12px; min-width: 30px;")
        layout.addWidget(self.value_label)
    
    def _on_value_changed(self, value: int):
        self._update_label(value)
        self.value_changed.emit(value)
    
    def _update_label(self, value: int):
        self.value_label.setText(str(value))
    
    def value(self) -> int:
        return self.slider.value()
    
    def set_value(self, value: int):
        self.slider.setValue(value)

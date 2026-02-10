"""
Modern Theme System with Color Palette and Styles
"""
from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class ThemeColors:
    """Modern Color Palette"""
    # Primary Colors
    primary: str = "#6366f1"          # Indigo 500
    primary_hover: str = "#4f46e5"    # Indigo 600
    primary_light: str = "#818cf8"    # Indigo 400
    
    # Background Colors
    bg_primary: str = "#0f172a"       # Slate 900
    bg_secondary: str = "#1e293b"     # Slate 800
    bg_tertiary: str = "#334155"      # Slate 700
    bg_card: str = "#1e293b"          # Slate 800
    bg_hover: str = "#334155"         # Slate 700
    
    # Text Colors
    text_primary: str = "#f8fafc"     # Slate 50
    text_secondary: str = "#cbd5e1"   # Slate 300
    text_muted: str = "#64748b"       # Slate 500
    text_disabled: str = "#475569"    # Slate 600
    
    # Accent Colors
    accent_success: str = "#22c55e"   # Green 500
    accent_warning: str = "#f59e0b"   # Amber 500
    accent_error: str = "#ef4444"     # Red 500
    accent_info: str = "#3b82f6"      # Blue 500
    
    # Border Colors
    border: str = "#334155"           # Slate 700
    border_light: str = "#475569"     # Slate 600
    
    # Status Colors
    status_active: str = "#22c55e"    # Green 500
    status_processing: str = "#3b82f6" # Blue 500
    status_warning: str = "#f59e0b"   # Amber 500
    status_error: str = "#ef4444"     # Red 500


class ModernTheme:
    """Modern Theme Generator with CSS-like Styles"""
    
    def __init__(self, colors: Optional[ThemeColors] = None):
        self.colors = colors or ThemeColors()
        self._cache: Dict[str, str] = {}
    
    def get_stylesheet(self) -> str:
        """Generate complete application stylesheet"""
        if 'full' in self._cache:
            return self._cache['full']
        
        styles = []
        styles.extend([
            self._main_window_style(),
            self._sidebar_style(),
            self._toolbar_style(),
            self._button_style(),
            self._input_style(),
            self._panel_style(),
            self._menu_style(),
            self._scrollbar_style(),
            self._tooltip_style(),
            self._progress_style(),
        ])
        
        self._cache['full'] = '\n'.join(styles)
        return self._cache['full']
    
    def _main_window_style(self) -> str:
        return f"""
        QMainWindow {{
            background-color: {self.colors.bg_primary};
            color: {self.colors.text_primary};
            border: none;
        }}
        
        QWidget {{
            background-color: {self.colors.bg_primary};
            color: {self.colors.text_primary};
            font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
            font-size: 13px;
        }}
        """
    
    def _sidebar_style(self) -> str:
        return f"""
        #ModernSidebar {{
            background-color: {self.colors.bg_secondary};
            border-right: 1px solid {self.colors.border};
        }}
        
        #SidebarBtn {{
            background-color: transparent;
            color: {self.colors.text_secondary};
            border: none;
            border-radius: 8px;
            padding: 8px;
        }}
        
        #SidebarBtn:hover {{
            background-color: {self.colors.bg_hover};
            color: {self.colors.text_primary};
        }}
        
        #SidebarBtn:checked {{
            background-color: {self.colors.primary};
            color: white;
        }}
        """
    
    def _toolbar_style(self) -> str:
        return f"""
        QToolBar {{
            background-color: {self.colors.bg_secondary};
            border: none;
            spacing: 4px;
            padding: 4px;
        }}
        
        QToolButton {{
            background-color: transparent;
            color: {self.colors.text_secondary};
            border: none;
            border-radius: 6px;
            padding: 6px;
        }}
        
        QToolButton:hover {{
            background-color: {self.colors.bg_hover};
            color: {self.colors.text_primary};
        }}
        
        QToolButton:checked {{
            background-color: {self.colors.primary};
            color: white;
        }}
        """
    
    def _button_style(self) -> str:
        return f"""
        QPushButton {{
            background-color: {self.colors.bg_tertiary};
            color: {self.colors.text_primary};
            border: 1px solid {self.colors.border};
            border-radius: 6px;
            padding: 8px 16px;
            font-weight: 500;
        }}
        
        QPushButton:hover {{
            background-color: {self.colors.bg_hover};
            border-color: {self.colors.border_light};
        }}
        
        QPushButton:pressed {{
            background-color: {self.colors.primary};
        }}
        
        QPushButton:disabled {{
            background-color: {self.colors.bg_secondary};
            color: {self.colors.text_disabled};
            border-color: {self.colors.border};
        }}
        
        QPushButton#PrimaryButton {{
            background-color: {self.colors.primary};
            color: white;
            border: none;
        }}
        
        QPushButton#PrimaryButton:hover {{
            background-color: {self.colors.primary_hover};
        }}
        """
    
    def _input_style(self) -> str:
        return f"""
        QLineEdit, QTextEdit, QPlainTextEdit {{
            background-color: {self.colors.bg_secondary};
            color: {self.colors.text_primary};
            border: 1px solid {self.colors.border};
            border-radius: 6px;
            padding: 8px;
            selection-background-color: {self.colors.primary};
        }}
        
        QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
            border-color: {self.colors.primary};
        }}
        
        QComboBox {{
            background-color: {self.colors.bg_secondary};
            color: {self.colors.text_primary};
            border: 1px solid {self.colors.border};
            border-radius: 6px;
            padding: 6px 12px;
        }}
        
        QComboBox:hover {{
            border-color: {self.colors.border_light};
        }}
        
        QComboBox::drop-down {{
            border: none;
            width: 20px;
        }}
        
        QComboBox QAbstractItemView {{
            background-color: {self.colors.bg_secondary};
            color: {self.colors.text_primary};
            border: 1px solid {self.colors.border};
            selection-background-color: {self.colors.primary};
        }}
        """
    
    def _panel_style(self) -> str:
        return f"""
        #ConfigPanel, #TextPanel {{
            background-color: {self.colors.bg_secondary};
            border: 1px solid {self.colors.border};
            border-radius: 8px;
        }}
        
        QGroupBox {{
            background-color: {self.colors.bg_secondary};
            color: {self.colors.text_primary};
            border: 1px solid {self.colors.border};
            border-radius: 8px;
            margin-top: 12px;
            padding-top: 12px;
            font-weight: 600;
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 12px;
            padding: 0 8px;
            color: {self.colors.text_secondary};
        }}
        """
    
    def _menu_style(self) -> str:
        return f"""
        QMenuBar {{
            background-color: {self.colors.bg_secondary};
            color: {self.colors.text_primary};
            border-bottom: 1px solid {self.colors.border};
        }}
        
        QMenuBar::item:selected {{
            background-color: {self.colors.bg_hover};
        }}
        
        QMenu {{
            background-color: {self.colors.bg_secondary};
            color: {self.colors.text_primary};
            border: 1px solid {self.colors.border};
            border-radius: 6px;
            padding: 6px;
        }}
        
        QMenu::item {{
            padding: 6px 24px;
            border-radius: 4px;
        }}
        
        QMenu::item:selected {{
            background-color: {self.colors.primary};
        }}
        
        QMenu::separator {{
            height: 1px;
            background-color: {self.colors.border};
            margin: 6px 0;
        }}
        """
    
    def _scrollbar_style(self) -> str:
        return f"""
        QScrollBar:vertical {{
            background-color: {self.colors.bg_secondary};
            width: 10px;
            border-radius: 5px;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {self.colors.bg_tertiary};
            border-radius: 5px;
            min-height: 20px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {self.colors.border_light};
        }}
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
        
        QScrollBar:horizontal {{
            background-color: {self.colors.bg_secondary};
            height: 10px;
            border-radius: 5px;
        }}
        
        QScrollBar::handle:horizontal {{
            background-color: {self.colors.bg_tertiary};
            border-radius: 5px;
            min-width: 20px;
        }}
        """
    
    def _tooltip_style(self) -> str:
        return f"""
        QToolTip {{
            background-color: {self.colors.bg_tertiary};
            color: {self.colors.text_primary};
            border: 1px solid {self.colors.border};
            border-radius: 4px;
            padding: 4px 8px;
        }}
        """
    
    def _progress_style(self) -> str:
        return f"""
        QProgressBar {{
            background-color: {self.colors.bg_secondary};
            color: {self.colors.text_primary};
            border: 1px solid {self.colors.border};
            border-radius: 4px;
            text-align: center;
        }}
        
        QProgressBar::chunk {{
            background-color: {self.colors.primary};
            border-radius: 3px;
        }}
        """

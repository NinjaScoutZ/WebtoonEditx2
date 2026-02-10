"""
Modern Theme System - Ultra Dark & Professional
"""
from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class ThemeColors:
    """Ultra Modern Color Palette - Deep Dark Edition"""
    # Primary & Accents
    primary: str = "#6366f1"          # Indigo 500
    primary_hover: str = "#4f46e5"    # Indigo 600
    primary_glow: str = "rgba(99, 102, 241, 0.4)"
    primary_soft: str = "rgba(99, 102, 241, 0.1)"
    
    # Deep Dark Backgrounds
    bg_base: str = "#020617"          # Slate 950
    bg_surface: str = "#0f172a"       # Slate 900
    bg_surface_light: str = "#1e293b" # Slate 800
    bg_glass: str = "rgba(15, 23, 42, 0.8)"
    
    # Text
    text_main: str = "#f8fafc"        # Slate 50
    text_sub: str = "#94a3b8"         # Slate 400
    text_muted: str = "#475569"       # Slate 600
    
    # Borders & Lines
    border_subtle: str = "rgba(255, 255, 255, 0.05)"
    border_active: str = "rgba(99, 102, 241, 0.5)"
    
    # Functional
    success: str = "#10b981"
    error: str = "#ef4444"


class ModernTheme:
    """Ultra Modern Theme with refined CSS"""
    
    def __init__(self, colors: Optional[ThemeColors] = None):
        self.colors = colors or ThemeColors()
    
    def get_stylesheet(self) -> str:
        return "\n".join([
            self._base_style(),
            self._scroll_style(),
            self._button_style(),
            self._card_style(),
            self._input_style(),
            self._sidebar_style(),
            self._splitter_style(),
            self._tab_style(),
            self._menu_style()
        ])
    
    def _base_style(self) -> str:
        return f"""
        QMainWindow, QDialog, QWidget {{
            background-color: {self.colors.bg_base};
            color: {self.colors.text_main};
            font-family: 'Inter', 'Segoe UI', sans-serif;
        }}
        
        #CentralWidget {{
            background-color: {self.colors.bg_base};
        }}
        
        QLabel {{
            background-color: transparent;
            color: {self.colors.text_main};
        }}
        
        QLabel#SubText {{
            color: {self.colors.text_sub};
            font-size: 12px;
        }}
        """
    
    def _scroll_style(self) -> str:
        return f"""
        QScrollBar:vertical {{
            background: transparent;
            width: 6px;
            margin: 0px;
        }}
        QScrollBar::handle:vertical {{
            background: {self.colors.text_muted};
            border-radius: 3px;
            min-height: 40px;
        }}
        QScrollBar::handle:vertical:hover {{
            background: {self.colors.text_sub};
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0px; }}
        """
    
    def _button_style(self) -> str:
        return f"""
        QPushButton {{
            background-color: {self.colors.bg_surface_light};
            border: 1px solid {self.colors.border_subtle};
            border-radius: 10px;
            padding: 10px 20px;
            color: {self.colors.text_main};
            font-weight: 600;
        }}
        QPushButton:hover {{
            background-color: rgba(255, 255, 255, 0.05);
            border-color: {self.colors.text_muted};
        }}
        QPushButton#PrimaryButton {{
            background-color: {self.colors.primary};
            border: none;
            color: white;
        }}
        QPushButton#PrimaryButton:hover {{
            background-color: {self.colors.primary_hover};
        }}
        """
    
    def _card_style(self) -> str:
        return f"""
        #ModernCard {{
            background-color: {self.colors.bg_surface};
            border: 1px solid {self.colors.border_subtle};
            border-radius: 16px;
        }}
        #CardTitle {{
            font-weight: 700;
            font-size: 14px;
            color: {self.colors.text_main};
            padding-bottom: 4px;
        }}
        """

    def _input_style(self) -> str:
        return f"""
        QLineEdit, QTextEdit {{
            background-color: {self.colors.bg_base};
            border: 1px solid {self.colors.border_subtle};
            border-radius: 8px;
            padding: 12px;
            color: {self.colors.text_main};
        }}
        QLineEdit:focus {{
            border-color: {self.colors.primary};
            background-color: {self.colors.bg_surface};
        }}
        """
    
    def _sidebar_style(self) -> str:
        return f"""
        #ModernSidebar {{
            background-color: {self.colors.bg_base};
            border-right: 1px solid {self.colors.border_subtle};
        }}
        #SidebarBtn {{
            border-radius: 12px;
            margin: 4px;
        }}
        #SidebarBtn:hover {{
            background-color: rgba(255, 255, 255, 0.05);
        }}
        #SidebarBtn:checked {{
            background-color: {self.colors.primary_soft};
            border: 1px solid {self.colors.primary};
        }}
        """

    def _splitter_style(self) -> str:
        return f"""
        QSplitter::handle {{
            background-color: {self.colors.border_subtle};
        }}
        """
    
    def _tab_style(self) -> str:
        return f"""
        QTabWidget::pane {{ border: none; }}
        QTabBar::tab {{
            background: transparent;
            color: {self.colors.text_sub};
            padding: 12px 24px;
            border-bottom: 2px solid transparent;
        }}
        QTabBar::tab:selected {{
            color: {self.colors.primary};
            border-bottom: 2px solid {self.colors.primary};
            font-weight: 700;
        }}
        """
    
    def _menu_style(self) -> str:
        return f"""
        QMenu {{
            background-color: {self.colors.bg_surface};
            border: 1px solid {self.colors.border_subtle};
            border-radius: 8px;
            padding: 4px;
        }}
        QMenu::item {{
            padding: 8px 32px;
            border-radius: 4px;
        }}
        QMenu::item:selected {{
            background-color: {self.colors.primary};
        }}
        """

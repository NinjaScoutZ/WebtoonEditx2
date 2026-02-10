"""
Modern Theme System with Color Palette and Styles
"""
from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class ThemeColors:
    """Modern Color Palette - Refined Slate & Indigo"""
    # Primary Colors
    primary: str = "#6366f1"          # Indigo 500
    primary_hover: str = "#4f46e5"    # Indigo 600
    primary_light: str = "#818cf8"    # Indigo 400
    primary_soft: str = "rgba(99, 102, 241, 0.15)"
    
    # Background Colors
    bg_primary: str = "#0f172a"       # Slate 900
    bg_secondary: str = "#1e293b"     # Slate 800
    bg_tertiary: str = "#334155"      # Slate 700
    bg_darker: str = "#020617"        # Slate 950
    bg_card: str = "#1e293b"          # Slate 800
    bg_hover: str = "rgba(255, 255, 255, 0.05)"
    
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
    border: str = "rgba(255, 255, 255, 0.08)"
    border_focus: str = "#6366f1"
    border_light: str = "rgba(255, 255, 255, 0.15)"


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
            self._splitter_style(),
            self._tab_style(),
            self._list_style(),
        ])
        
        self._cache['full'] = '\n'.join(styles)
        return self._cache['full']
    
    def _main_window_style(self) -> str:
        return f"""
        QMainWindow {{
            background-color: {self.colors.bg_primary};
            color: {self.colors.text_primary};
        }}
        
        QWidget {{
            background-color: transparent;
            color: {self.colors.text_primary};
            font-family: 'Inter', 'Segoe UI', 'Microsoft YaHei', sans-serif;
            font-size: 13px;
        }}

        #CentralWidget {{
            background-color: {self.colors.bg_primary};
        }}
        """
    
    def _sidebar_style(self) -> str:
        return f"""
        #ModernSidebar {{
            background-color: {self.colors.bg_darker};
            border-right: 1px solid {self.colors.border};
        }}
        
        #SidebarBtn {{
            background-color: transparent;
            color: {self.colors.text_secondary};
            border: none;
            border-radius: 12px;
            padding: 8px;
        }}
        
        #SidebarBtn:hover {{
            background-color: {self.colors.bg_hover};
            color: {self.colors.text_primary};
        }}
        
        #SidebarBtn:checked {{
            background-color: {self.colors.primary_soft};
            color: {self.colors.primary_light};
            border: 1px solid {self.colors.primary};
        }}
        """
    
    def _toolbar_style(self) -> str:
        return f"""
        QToolBar {{
            background-color: {self.colors.bg_secondary};
            border: none;
            border-bottom: 1px solid {self.colors.border};
            spacing: 6px;
            padding: 6px;
        }}
        
        QToolButton {{
            background-color: transparent;
            color: {self.colors.text_secondary};
            border: none;
            border-radius: 8px;
            padding: 6px;
        }}
        
        QToolButton:hover {{
            background-color: {self.colors.bg_hover};
        }}
        
        QToolButton:checked {{
            background-color: {self.colors.primary_soft};
            color: {self.colors.primary_light};
        }}
        """
    
    def _button_style(self) -> str:
        return f"""
        QPushButton {{
            background-color: {self.colors.bg_tertiary};
            color: {self.colors.text_primary};
            border: 1px solid {self.colors.border};
            border-radius: 10px;
            padding: 8px 16px;
            font-weight: 500;
        }}
        
        QPushButton:hover {{
            background-color: {self.colors.bg_hover};
            border-color: {self.colors.border_light};
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
            background-color: {self.colors.bg_darker};
            color: {self.colors.text_primary};
            border: 1px solid {self.colors.border};
            border-radius: 8px;
            padding: 10px;
            selection-background-color: {self.colors.primary};
        }}
        
        QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
            border-color: {self.colors.primary};
            background-color: {self.colors.bg_secondary};
        }}
        
        QComboBox {{
            background-color: {self.colors.bg_secondary};
            border: 1px solid {self.colors.border};
            border-radius: 8px;
            padding: 6px 12px;
        }}
        """
    
    def _scrollbar_style(self) -> str:
        return f"""
        QScrollBar:vertical {{
            background-color: transparent;
            width: 8px;
            margin: 0px;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {self.colors.bg_tertiary};
            border-radius: 4px;
            min-height: 20px;
            margin: 2px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {self.colors.text_muted};
        }}
        
        QScrollBar:horizontal {{
            background-color: transparent;
            height: 8px;
            margin: 0px;
        }}
        
        QScrollBar::handle:horizontal {{
            background-color: {self.colors.bg_tertiary};
            border-radius: 4px;
            min-width: 20px;
            margin: 2px;
        }}
        """

    def _splitter_style(self) -> str:
        return f"""
        QSplitter::handle {{
            background-color: {self.colors.border};
        }}
        
        QSplitter::handle:horizontal {{
            width: 1px;
        }}
        
        QSplitter::handle:vertical {{
            height: 1px;
        }}
        """
    
    def _tab_style(self) -> str:
        return f"""
        QTabWidget::pane {{
            border: 1px solid {self.colors.border};
            border-radius: 8px;
            top: -1px;
            background-color: {self.colors.bg_secondary};
        }}
        
        QTabBar::tab {{
            background-color: transparent;
            color: {self.colors.text_secondary};
            padding: 10px 20px;
            border-bottom: 2px solid transparent;
        }}
        
        QTabBar::tab:selected {{
            color: {self.colors.primary_light};
            border-bottom: 2px solid {self.colors.primary};
            font-weight: 600;
        }}
        
        QTabBar::tab:hover:!selected {{
            background-color: {self.colors.bg_hover};
        }}
        """
    
    def _list_style(self) -> str:
        return f"""
        QListWidget, QTreeWidget, QTableView {{
            background-color: {self.colors.bg_darker};
            border: 1px solid {self.colors.border};
            border-radius: 8px;
            outline: none;
        }}

        QListWidget::item, QTreeWidget::item {{
            padding: 8px;
            border-radius: 6px;
            margin: 2px 4px;
        }}
        
        QListWidget::item:selected, QTreeWidget::item:selected {{
            background-color: {self.colors.primary_soft};
            color: {self.colors.primary_light};
        }}

        QListWidget::item:hover:!selected, QTreeWidget::item:hover:!selected {{
            background-color: {self.colors.bg_hover};
        }}
        """

    def _panel_style(self) -> str: return ""
    def _menu_style(self) -> str: return ""
    def _tooltip_style(self) -> str: return ""
    def _progress_style(self) -> str: return ""

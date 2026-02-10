"""
Modern Launcher - Entry point for the new UI
"""
import sys
import os
import argparse
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Load configuration FIRST (before any imports that use pcfg)
from utils.config import load_config
load_config()

# Import pcfg AFTER load_config to get the initialized value
from utils.config import pcfg

# Now import other modules
from utils import shared

def main():
    parser = argparse.ArgumentParser(description='Modern Manga Translator')
    parser.add_argument('--proj-dir', default='', type=str, help='Open project directory on startup')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    args = parser.parse_args()
    
    # Qt imports
    from qtpy.QtWidgets import QApplication
    from qtpy.QtCore import Qt
    from qtpy.QtGui import QFont
    
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("Modern Manga Translator")
    app.setApplicationVersion("2.0.0")
    
    # Enable High DPI
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    # Set default font
    font = QFont("Segoe UI", 10)
    if not QFont(font).exactMatch():
        font = QFont("Microsoft YaHei UI", 10)
    app.setFont(font)
    
    # Import main window after config is loaded
    from ui.main_window_new import ModernMainWindow
    
    # Set shared paths
    shared.PROGRAM_PATH = str(Path(__file__).parent)
    shared.LOGGING_PATH = str(Path(__file__).parent / 'logs')
    
    # Create and show main window
    window = ModernMainWindow(app, pcfg, open_dir=args.proj_dir)
    
    # Run application
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

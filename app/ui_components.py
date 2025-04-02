# app/ui_components.py
# Custom UI components

from PyQt5.QtWidgets import QPushButton, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from .theme_manager import ThemeManager

class ModernButton(QPushButton):
    """Custom modern button"""
    def __init__(self, text, parent=None, color="#5c6bc0", hover_color="#7986cb", is_dark_mode=False):
        super().__init__(text, parent)
        self.color = color
        self.hover_color = hover_color
        self.is_dark_mode = is_dark_mode
        self.setMouseTracking(True)
        self.setMinimumHeight(42)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.update_style()
    
    def update_style(self):
        """Update button style"""
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.color};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: {self.hover_color};
            }}
            QPushButton:pressed {{
                background-color: {self.color};
            }}
        """)
    
    def set_dark_mode(self, is_dark_mode):
        """Set button dark mode"""
        self.is_dark_mode = is_dark_mode
        # If button colors need to be changed based on dark mode, it can be implemented here
        self.update_style()


class ModernLineEdit(QLineEdit):
    """Custom modern input field"""
    def __init__(self, parent=None, is_dark_mode=False):
        super().__init__(parent)
        self.is_dark_mode = is_dark_mode
        self.setMinimumHeight(34)
        self.update_style()
    
    def update_style(self):
        """Update input field style"""
        # Get theme colors
        theme = ThemeManager.get_theme(self.is_dark_mode)
        
        self.setStyleSheet(f"""
            QLineEdit {{
                border: 1px solid {theme['input_border']};
                border-radius: 5px;
                padding: 7px 10px;
                background-color: {theme['input_bg']};
                color: {theme['text_color']};
                selection-background-color: #7986cb;
                font-size: 13px;
            }}
            QLineEdit:focus {{
                border: 1px solid {theme['input_focus_border']};
            }}
        """)
    
    def set_dark_mode(self, is_dark_mode):
        """Set input field dark mode"""
        self.is_dark_mode = is_dark_mode
        self.update_style()
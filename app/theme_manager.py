# app/theme_manager.py
# Responsible for managing application themes and styles

class ThemeManager:
    """Theme management class, provides colors and styles for day/night modes"""
    
    @staticmethod
    def get_theme(is_dark_mode=False):
        """Get theme colors and styles"""
        if is_dark_mode:
            return {
                # Main background and text colors
                'bg_color': '#2c2c2c',
                'text_color': '#ffffff',
                'secondary_text': '#b0b0b0',
                
                # Container and element colors
                'container_bg': '#3c3c3c',
                'container_border': '#505050',
                
                # Button colors (dark versions of indigo, purple, teal)
                'btn_colors': [
                    ("#3949ab", "#5c6bc0"),  # Indigo
                    ("#7b1fa2", "#9c27b0"),  # Purple
                    ("#00695c", "#00897b"),  # Teal
                ],
                
                # Input field colors
                'input_bg': '#3c3c3c',
                'input_border': '#505050',
                'input_focus_border': '#5c6bc0',
                
                # Separator color
                'separator': '#505050',
                
                # Global style
                'global_style': """
                    QMainWindow, QDialog, QScrollArea, QWidget {
                        background-color: #2c2c2c;
                        color: #ffffff;
                        font-family: 'Microsoft YaHei', 'PingFang SC', sans-serif;
                    }
                    QScrollArea {
                        border: none;
                    }
                    QCheckBox, QRadioButton {
                        color: #ffffff;
                    }
                    QCheckBox::indicator:unchecked, QRadioButton::indicator:unchecked {
                        border: 2px solid #7986cb;
                        background-color: #3c3c3c;
                        border-radius: 4px;
                    }
                    QCheckBox::indicator:checked, QRadioButton::indicator:checked {
                        background-color: #5c6bc0;
                        border: 2px solid #5c6bc0;
                        border-radius: 4px;
                    }
                """
            }
        else:
            return {
                # Main background and text colors
                'bg_color': '#f5f7ff',
                'text_color': '#424242',
                'secondary_text': '#5c6bc0',
                
                # Container and element colors
                'container_bg': '#ffffff',
                'container_border': '#e0e0e0',
                
                # Button colors
                'btn_colors': [
                    ("#3949ab", "#5c6bc0"),  # Indigo
                    ("#7b1fa2", "#9c27b0"),  # Purple
                    ("#00695c", "#00897b"),  # Teal
                ],
                
                # Input field colors
                'input_bg': '#ffffff',
                'input_border': '#e0e0e0',
                'input_focus_border': '#5c6bc0',
                
                # Separator color
                'separator': '#e0e0e0',
                
                # Global style
                'global_style': """
                    QMainWindow, QDialog, QScrollArea, QWidget {
                        background-color: #f5f7ff;
                        color: #424242;
                        font-family: 'Microsoft YaHei', 'PingFang SC', sans-serif;
                    }
                    QScrollArea {
                        border: none;
                    }
                    QCheckBox::indicator:unchecked, QRadioButton::indicator:unchecked {
                        border: 2px solid #9fa8da;
                        background-color: white;
                        border-radius: 4px;
                    }
                    QCheckBox::indicator:checked, QRadioButton::indicator:checked {
                        background-color: #3949ab;
                        border: 2px solid #3949ab;
                        border-radius: 4px;
                    }
                """
            }
    
    @staticmethod
    def get_message_box_style(is_dark_mode=False):
        """Get message box style"""
        theme = ThemeManager.get_theme(is_dark_mode)
        return f"""
            QMessageBox {{
                background-color: {theme['bg_color']};
            }}
            QMessageBox QLabel {{
                color: {theme['text_color']};
                font-size: 14px;
            }}
            QMessageBox QPushButton {{
                background-color: {theme['btn_colors'][0][0]};
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 16px;
                font-weight: bold;
                min-width: 80px;
                min-height: 30px;
            }}
            QMessageBox QPushButton:hover {{
                background-color: {theme['btn_colors'][0][1]};
            }}
        """
    
    @staticmethod
    def get_error_message_box_style(is_dark_mode=False):
        """Get error message box style"""
        theme = ThemeManager.get_theme(is_dark_mode)
        return f"""
            QMessageBox {{
                background-color: {theme['bg_color']};
            }}
            QMessageBox QLabel {{
                color: {theme['text_color']};
                font-size: 14px;
            }}
            QMessageBox QPushButton {{
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 16px;
                font-weight: bold;
                min-width: 80px;
                min-height: 30px;
            }}
            QMessageBox QPushButton:hover {{
                background-color: #e53935;
            }}
        """
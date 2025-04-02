# app/floating_window.py
# Floating window implementation (horizontal layout)

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QLabel, QPushButton, QFrame, QDesktopWidget)
from PyQt5.QtCore import Qt, QPoint
from .ui_components import ModernButton
from .theme_manager import ThemeManager
from PyQt5.QtGui import QIcon
import os

class FloatingWindow(QMainWindow):
    """Floating window (horizontal layout)"""
    def __init__(self, parent=None, programs=None, switch_callback=None, is_dark_mode=False):
        super().__init__(parent, Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)

        self.programs = programs or []
        self.switch_callback = switch_callback
        self.is_dark_mode = is_dark_mode
        self.setWindowTitle("Quick Switch")
        self.setMinimumWidth(150)
        # Set application icon
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resources', 'app_icon.ico')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # Calculate window size (horizontal design)
        self.calculate_window_size()
        
        # Track mouse events for dragging
        self.dragging = False
        self.offset = QPoint()
        
        # Set up UI
        self.init_ui()
    
    
    def calculate_window_size(self):
        """Calculate window size (ensure all buttons are fully displayed)"""
        # Filter out empty program names
        active_programs = [p for p in self.programs if p]
        program_count = len(active_programs)
        
        # Set appropriate base values
        button_width = 120      # Base width for each button
        window_padding = 40     # Window padding on both sides (increased)
        title_extra_space = 40  # Extra space for title bar and close button
        button_margin = 10      # Margin between buttons
        
        # Minimum window size
        min_width = 200  # Increased minimum width to ensure enough display space
        min_height = 90  # Increased minimum height to ensure enough display space
        
        if program_count > 0:
            # Calculate total width needed: button width + button margins + window padding + title bar extra space
            needed_width = (program_count * button_width) + ((program_count - 1) * button_margin) + window_padding + title_extra_space
        
            # Ensure width is not less than minimum width and not greater than maximum width
            width = min(800, max(min_width, needed_width))
            height = min_height  # Fixed height, ensure it's enough
        else:
            width = min_width
            height = min_height
        
        # Set window position (above the bottom-right corner)
        desktop = QDesktopWidget().availableGeometry()
        x = desktop.width() - width - 20
        y = desktop.height() - height - 80  # Above the taskbar
        
        self.setGeometry(x, y, width, height)
        print(f"FloatingWindow size: {width}x{height}, Program count: {program_count}")

    # Modified button creation part in init_ui method

    def init_ui(self):
        """Initialize interface (horizontal layout and ensure buttons are fully displayed)"""
        # Get theme colors
        theme = ThemeManager.get_theme(self.is_dark_mode)
        
        # Set background
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {theme['bg_color']};
                border: 1px solid {theme['container_border']};
                border-radius: 8px;
            }}
        """)
        
        # Main container
        container = QWidget()
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(10, 5, 10, 5)
        main_layout.setSpacing(5)
        
        # Title area
        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(5, 0, 5, 0)
        title_layout.setSpacing(5)
        
        # Title
        title_label = QLabel("Program Switch")
        title_label.setStyleSheet(f"font-weight: bold; color: {theme['secondary_text']};")
        
        # Close button
        close_button = QPushButton("×")
        close_button.setFixedSize(20, 20)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #ff5252;
                color: white;
                border-radius: 10px;
                font-weight: bold;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: #ff1744;
            }
        """)
        close_button.clicked.connect(self.hide)
        
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        title_layout.addWidget(close_button)
        
        main_layout.addLayout(title_layout)
        
        # Separator line
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet(f"background-color: {theme['separator']};")
        main_layout.addWidget(line)
        
        # Program buttons area (horizontal layout)
        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(5, 0, 5, 0)  # Increase left and right margins
        buttons_layout.setSpacing(10)  # Increase spacing between buttons
        buttons_layout.setAlignment(Qt.AlignCenter)  # Center alignment instead of left alignment
        
        # Filter out empty program names
        active_programs = [p for p in self.programs if p]
        
        # Create program buttons
        if active_programs:
            for program in active_programs:
                # Create unique color for each program
                colors = theme['btn_colors']
                index = active_programs.index(program) % 3
                
                button = ModernButton(program, color=colors[index][0], hover_color=colors[index][1], is_dark_mode=self.is_dark_mode)
                button.setFixedWidth(110)  # Fixed width to avoid automatic adjustment
                button.setFixedHeight(34)  # Fixed height
                button.clicked.connect(lambda checked, p=program: self.switch_callback(p))
                buttons_layout.addWidget(button)
        else:
            # If no programs, display a hint
            empty_label = QLabel("No programs set")
            empty_label.setStyleSheet(f"color: {theme['secondary_text']}; font-style: italic;")
            empty_label.setAlignment(Qt.AlignCenter)
            buttons_layout.addWidget(empty_label)
        
        main_layout.addLayout(buttons_layout)
        
        self.setCentralWidget(container)
    
    def mousePressEvent(self, event):
        """Click event, used for dragging the window"""
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.pos()
    
    def mouseMoveEvent(self, event):
        """Move event, used for dragging the window"""
        if self.dragging and event.buttons() & Qt.LeftButton:
            self.move(self.mapToGlobal(event.pos() - self.offset))
    
    def mouseReleaseEvent(self, event):
        """Release event, stop dragging"""
        if event.button() == Qt.LeftButton:
            self.dragging = False
    
    # Modify method for updating programs in floating window

    def update_programs(self, programs, is_dark_mode=None):
        """Update program list and theme"""
        
        # Update program list
        self.programs = programs
        
        # Update dark mode setting (if provided)
        if is_dark_mode is not None:
            self.is_dark_mode = is_dark_mode
        
        # Recalculate window size
        self.calculate_window_size()
        
        # Ensure window is in front
        self.raise_()
        self.activateWindow()
        
        # Clear and rebuild UI
        if self.centralWidget():
            old_widget = self.centralWidget()
            old_widget.setParent(None)
            old_widget.deleteLater()
        
        self.init_ui()
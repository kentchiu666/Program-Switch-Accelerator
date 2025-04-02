# app/main_window.py
# Main window implementation, simplified version

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QLabel, QMessageBox, QFrame, QCheckBox, QScrollArea,
                           QButtonGroup, QRadioButton)
from PyQt5.QtCore import Qt, QTimer

from .settings_manager import SettingsManager
from .window_manager import WindowManager
from .ui_components import ModernButton, ModernLineEdit
from .floating_window import FloatingWindow
from .theme_manager import ThemeManager
from .hotkey_manager import HotkeyManager


class ProgramSwitchAccelerator(QMainWindow):
    """Program Switch Accelerator main window class"""
    def __init__(self):
        super().__init__()
        
        # Initialize settings manager
        self.settings_manager = SettingsManager()
        
        # Initialize window manager
        self.window_manager = WindowManager()
        
        # Initialize hotkey manager
        self.hotkey_manager = HotkeyManager()
        self.hotkey_manager.hotkey_triggered.connect(self.switch_to_program)
        
        from main import APP_VERSION
        # Set window properties
        self.setWindowTitle(f"Program Switch Accelerator v{APP_VERSION}")
        self.setMinimumSize(450, 450)
        
        # Floating window
        self.float_window = None
        if self.settings_manager.float_window_enabled:
            self.init_float_window()
        
        # Set fixed hotkeys (basic version directly uses F1-F3)
        self.update_default_hotkeys()
        
        # Set up UI
        self.init_ui()
        
        # Start listening for hotkeys if enabled
        if self.settings_manager.hotkeys_enabled:
            self.hotkey_manager.start_listening()
    
    def update_default_hotkeys(self):
        """Update default hotkey settings (free version: F1-F3)"""
        print("Updating default hotkeys")
        hotkeys = {}
        for i, program in enumerate(self.settings_manager.programs):
            if program and i < 3:  # Free version only has 3 programs
                hotkeys[program] = f"F{i+1}"
                print(f"Setting hotkey F{i+1} for program: {program}")
        
        # Update hotkey mappings in the hotkey manager
        self.hotkey_manager.set_hotkeys(hotkeys)
        
        # Debug all hotkeys
        print(f"Current hotkeys: {hotkeys}")
        print(f"Hotkey manager status: running={self.hotkey_manager.running}, thread exists={(self.hotkey_manager.thread is not None)}")
        if self.hotkey_manager.thread:
            print(f"Hotkey thread active: {self.hotkey_manager.thread.is_alive()}")
    
    def check_hotkey_status(self):
        """Check hotkey status"""
        print("\n===== Hotkey Status Check =====")
        print(f"Hotkeys enabled: {self.settings_manager.hotkeys_enabled}")
        print(f"Hotkey manager running: {self.hotkey_manager.running}")
        print(f"Hotkey manager thread: {self.hotkey_manager.thread is not None}")
        if self.hotkey_manager.thread:
            print(f"Hotkey thread active: {self.hotkey_manager.thread.is_alive()}")
        print(f"Hotkey mappings: {self.hotkey_manager.hotkeys}")
        print("========================\n")
    
    def init_ui(self):
        """Initialize user interface"""
        # Get theme colors
        theme = ThemeManager.get_theme(self.settings_manager.is_dark_mode)
        
        # Set global style
        self.setStyleSheet(theme['global_style'])
        
        # Main components and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Title area
        title_widget = QWidget()
        title_layout = QVBoxLayout(title_widget)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(5)
        
        # Title label
        title_label = QLabel(f"Program Switch Accelerator")
        title_label.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {theme['secondary_text']};")
        title_label.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(title_label)
        
        # Subtitle/Version label
        version_label = QLabel(f"{self.settings_manager.version}")
        version_label.setStyleSheet(f"font-size: 14px; color: {theme['secondary_text']};")
        version_label.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(version_label)
        
        main_layout.addWidget(title_widget)
        
        # Separator line
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet(f"background-color: {theme['separator']}; margin: 5px 0;")
        main_layout.addWidget(separator)
        
        # Instruction label
        instruction_label = QLabel("Please enter the program names you want to quickly switch between")
        instruction_label.setStyleSheet(f"font-size: 14px; color: {theme['secondary_text']};")
        instruction_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(instruction_label)
        
        # Settings input area
        settings_widget = QWidget()
        settings_widget.setObjectName("settingsWidget")
        settings_widget.setStyleSheet(f"""
            #settingsWidget {{
                background-color: {theme['container_bg']};
                border-radius: 10px;
                border: 1px solid {theme['container_border']};
            }}
        """)
        settings_layout = QVBoxLayout(settings_widget)
        settings_layout.setContentsMargins(20, 15, 20, 15)
        settings_layout.setSpacing(12)
        
        # Program input boxes and labels
        self.program_entries = []
        for i in range(self.settings_manager.max_programs):
            row_widget = QWidget()
            row_layout = QHBoxLayout(row_widget)
            row_layout.setContentsMargins(0, 0, 0, 0)
            row_layout.setSpacing(10)
            
            label = QLabel(f"Program {i+1}:")
            if i < 3:  # Free version shows hotkey hint
                label.setStyleSheet(f"font-size: 14px; font-weight: bold; color: {theme['secondary_text']};")
            else:
                label.setStyleSheet(f"font-size: 14px; color: {theme['secondary_text']};")
            label.setMinimumWidth(80)
            
            entry = ModernLineEdit(is_dark_mode=self.settings_manager.is_dark_mode)
            if i < len(self.settings_manager.programs) and self.settings_manager.programs[i]:
                entry.setText(self.settings_manager.programs[i])
            
            # Show hotkey label for the first three programs
            if i < 3:
                hotkey_label = QLabel(f"[F{i+1}]")
                hotkey_label.setStyleSheet(f"font-size: 12px; color: {theme['secondary_text']}; font-style: italic;")
                row_layout.addWidget(label)
                row_layout.addWidget(entry)
                row_layout.addWidget(hotkey_label)
            else:
                row_layout.addWidget(label)
                row_layout.addWidget(entry)
            
            settings_layout.addWidget(row_widget)
            self.program_entries.append(entry)
        
        # Add feature options
        options_widget = QWidget()
        options_layout = QVBoxLayout(options_widget)
        options_layout.setContentsMargins(0, 10, 0, 0)
        options_layout.setSpacing(8)
        
        # Floating window option
        float_widget = QWidget()
        float_layout = QHBoxLayout(float_widget)
        float_layout.setContentsMargins(0, 0, 0, 0)
        
        self.float_checkbox = QCheckBox("Enable floating window")
        self.float_checkbox.setStyleSheet(f"""
            QCheckBox {{
                font-size: 14px;
                color: {theme['secondary_text']};
            }}
        """)
        self.float_checkbox.setChecked(self.settings_manager.float_window_enabled)
        
        float_layout.addWidget(self.float_checkbox)
        float_layout.addStretch()
        
        options_layout.addWidget(float_widget)
        
        # Hotkey option
        hotkey_widget = QWidget()
        hotkey_layout = QHBoxLayout(hotkey_widget)
        hotkey_layout.setContentsMargins(0, 0, 0, 0)
        
        self.hotkey_checkbox = QCheckBox("Enable keyboard shortcuts (F1-F3)")
        self.hotkey_checkbox.setStyleSheet(f"""
            QCheckBox {{
                font-size: 14px;
                color: {theme['secondary_text']};
            }}
        """)
        self.hotkey_checkbox.setChecked(self.settings_manager.hotkeys_enabled)
        
        hotkey_layout.addWidget(self.hotkey_checkbox)
        hotkey_layout.addStretch()
        
        options_layout.addWidget(hotkey_widget)
        
        # Theme option
        theme_widget = QWidget()
        theme_layout = QHBoxLayout(theme_widget)
        theme_layout.setContentsMargins(0, 0, 0, 0)
        
        theme_label = QLabel("Interface theme:")
        theme_label.setStyleSheet(f"font-size: 14px; color: {theme['secondary_text']};")
        
        self.theme_group = QButtonGroup(self)
        self.day_mode_radio = QRadioButton("Light mode")
        self.night_mode_radio = QRadioButton("Dark mode")
        
        if self.settings_manager.is_dark_mode:
            self.night_mode_radio.setChecked(True)
        else:
            self.day_mode_radio.setChecked(True)
        
        self.theme_group.addButton(self.day_mode_radio)
        self.theme_group.addButton(self.night_mode_radio)
        
        self.day_mode_radio.setStyleSheet(f"font-size: 13px; color: {theme['text_color']};")
        self.night_mode_radio.setStyleSheet(f"font-size: 13px; color: {theme['text_color']};")
        
        theme_layout.addWidget(theme_label)
        theme_layout.addWidget(self.day_mode_radio)
        theme_layout.addWidget(self.night_mode_radio)
        theme_layout.addStretch()
        
        options_layout.addWidget(theme_widget)
        
        settings_layout.addWidget(options_widget)
        
        # Add settings frame to main layout
        main_layout.addWidget(settings_widget)
        
        # Save button
        save_button = ModernButton("Save Settings", is_dark_mode=self.settings_manager.is_dark_mode)
        save_button.clicked.connect(self.save_settings)
        main_layout.addWidget(save_button)
        
        # Program switching buttons area title
        buttons_label = QLabel("Quick Switch")
        buttons_label.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {theme['secondary_text']}; margin-top: 5px;")
        buttons_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(buttons_label)
        
        # Program switching buttons container
        buttons_container = QWidget()
        buttons_container.setObjectName("buttonsContainer")
        buttons_container.setStyleSheet(f"""
            #buttonsContainer {{
                background-color: {theme['container_bg']};
                border-radius: 10px;
                border: 1px solid {theme['container_border']};
                min-height: 70px;
            }}
        """)
        
        # Create buttons area
        self.buttons_layout = QHBoxLayout(buttons_container)
        self.buttons_layout.setContentsMargins(15, 15, 15, 15)
        self.buttons_layout.setSpacing(10)
        self.buttons_layout.setAlignment(Qt.AlignCenter)
        
        # Create program switching buttons
        self.create_program_buttons()
        
        # Add buttons container to main layout
        main_layout.addWidget(buttons_container)
        
        # Bottom tip
        tip_text = "Tip: Press the corresponding function key (F1-F3) to quickly switch programs" if self.settings_manager.hotkeys_enabled else "Tip: Enable hotkeys to use function keys (F1-F3) for quick switching"
        self.tip_label = QLabel(tip_text)
        self.tip_label.setStyleSheet(f"font-size: 12px; color: {theme['secondary_text']}; font-style: italic;")
        self.tip_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.tip_label)

    
    def update_float_window(self, programs, enabled, is_dark_mode):
        """Update floating window"""
        # If floating window doesn't exist, create one
        if not self.float_window:
            self.float_window = FloatingWindow(
                programs=programs,
                switch_callback=self.switch_to_program,
                is_dark_mode=is_dark_mode
            )
        else:
            # Completely rebuild floating window to ensure all changes are applied
            self.float_window.close()
            self.float_window = FloatingWindow(
                programs=programs,
                switch_callback=self.switch_to_program,
                is_dark_mode=is_dark_mode
            )
        
        # Show or hide floating window based on settings
        if enabled:
            self.float_window.show()
        else:
            self.float_window.hide()
    
    def init_float_window(self):
        """Initialize floating window"""
        self.update_float_window(
            self.settings_manager.programs,
            self.settings_manager.float_window_enabled,
            self.settings_manager.is_dark_mode
        )
    
    def create_program_buttons(self):
        """Create program switching buttons"""
        # Clear existing buttons
        while self.buttons_layout.count():
            item = self.buttons_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        
        # Get theme colors
        theme = ThemeManager.get_theme(self.settings_manager.is_dark_mode)
        
        # Create buttons for each configured program
        for i, program in enumerate(self.settings_manager.programs):
            if program:
                # Use different colors for each program
                colors = theme['btn_colors']
                
                index = i % 3
                button = ModernButton(program, color=colors[index][0], hover_color=colors[index][1], is_dark_mode=self.settings_manager.is_dark_mode)
                button.setMinimumWidth(110)
                
                # Show hotkey label for the first three programs if hotkeys are enabled
                if i < 3 and self.settings_manager.hotkeys_enabled:
                    button.setText(f"{program}\n[F{i+1}]")
                
                button.clicked.connect(lambda checked, p=program: self.switch_to_program(p))
                self.buttons_layout.addWidget(button)
        
        # If no programs are set, show a hint
        if not any(self.settings_manager.programs):
            empty_label = QLabel("No programs set")
            empty_label.setStyleSheet(f"color: {theme['secondary_text']}; font-style: italic;")
            empty_label.setAlignment(Qt.AlignCenter)
            self.buttons_layout.addWidget(empty_label)
    
    def save_settings(self):
        """Save settings"""
        # Get program names from input boxes
        programs = []
        for entry in self.program_entries:
            program_name = entry.text().strip()
            programs.append(program_name)
        
        # Get floating window status
        float_window_enabled = self.float_checkbox.isChecked()
        
        # Get hotkey enabled status
        hotkeys_enabled = self.hotkey_checkbox.isChecked()
        
        # Get theme setting
        is_dark_mode = self.night_mode_radio.isChecked()
        
        # Check if settings have changed
        programs_changed = programs != self.settings_manager.programs
        hotkeys_changed = hotkeys_enabled != self.settings_manager.hotkeys_enabled
        float_window_changed = float_window_enabled != self.settings_manager.float_window_enabled
        theme_changed = is_dark_mode != self.settings_manager.is_dark_mode
        
        # Check if any settings have changed
        settings_changed = programs_changed or hotkeys_changed or float_window_changed or theme_changed
        
        if settings_changed:
            print("Settings have changed, saving...")
            # First save settings to settings_manager
            self.settings_manager.save_settings(
                programs, 
                float_window_enabled, 
                is_dark_mode,
                hotkeys_enabled
            )
            
            # =================Hotkey Update Logic=================
            # If hotkey settings or program list has changed, update hotkeys
            if hotkeys_changed or (programs_changed and hotkeys_enabled):
                print("Updating hotkey settings")
                # Stop current hotkey listening
                if self.hotkey_manager.running:
                    print("Stopping existing hotkey listener")
                    self.hotkey_manager.stop_listening()
                
                # Update hotkey mappings
                self.update_default_hotkeys()
                
                # If hotkeys need to be enabled, start listening
                if hotkeys_enabled:
                    print("Starting hotkey listener")
                    self.hotkey_manager.start_listening()
                    
                # Debug hotkey status
                self.check_hotkey_status()
            
            # =================Floating Window Update Logic=================
            # If floating window settings or program list has changed, update floating window
            if float_window_changed or programs_changed or theme_changed:
                print("Updating floating window")
                self.update_float_window(programs, float_window_enabled, is_dark_mode)
            
            # =================Theme Update Logic=================
            # If theme has changed, update UI without rebuilding the window
            if theme_changed:
                print("Updating theme")
                # Remember current program list and settings
                current_programs = self.settings_manager.programs
                current_float_enabled = self.settings_manager.float_window_enabled
                current_hotkeys_enabled = self.settings_manager.hotkeys_enabled
                
                # Remember window position and size
                geometry = self.geometry()
                
                # Stop hotkey listening
                if self.hotkey_manager and current_hotkeys_enabled:
                    self.hotkey_manager.stop_listening()
                
                # Close floating window
                if self.float_window:
                    self.float_window.close()
                    self.float_window = None
                
                # Apply new theme to existing window, rather than creating a new window
                theme = ThemeManager.get_theme(is_dark_mode)
                self.setStyleSheet(theme['global_style'])
                
                # Reinitialize UI
                # Clear current UI
                central_widget = self.centralWidget()
                if central_widget:
                    central_widget.deleteLater()
                
                # Reinitialize UI
                self.init_ui()
                
                # Reapply geometry
                self.setGeometry(geometry)
                
                # Reset hotkeys and floating window
                if current_hotkeys_enabled:
                    self.update_default_hotkeys()
                    self.hotkey_manager.start_listening()
                
                if current_float_enabled:
                    self.init_float_window()
                
                # Use delayed display of success message to avoid UI issues
                def show_success_message():
                    msg = QMessageBox(self)
                    msg.setWindowTitle("Success")
                    msg.setText("Settings Saved")
                    msg.setIcon(QMessageBox.Information)
                    msg.setStyleSheet(ThemeManager.get_message_box_style(is_dark_mode))
                    msg.setModal(False)  # Set as non-modal dialog
                    msg.exec_()
                
                QTimer.singleShot(200, show_success_message)
                return  # Early return to avoid showing the message box twice
            else:
                # Only update program switching buttons
                self.create_program_buttons()
                
                # Update bottom tip text
                tip_text = "Tip: Press the corresponding function key (F1-F3) to quickly switch programs" if hotkeys_enabled else "Tip: Enable hotkeys to use function keys (F1-F3) for quick switching"
                self.tip_label.setText(tip_text)
            
            # Use delayed display of success message to avoid UI issues
            def show_success_message():
                msg = QMessageBox(self)
                msg.setWindowTitle("Success")
                msg.setText("Settings Saved")
                msg.setIcon(QMessageBox.Information)
                msg.setStyleSheet(ThemeManager.get_message_box_style(is_dark_mode))
                msg.setModal(False)  # Set as non-modal dialog
                msg.exec_()
            
            QTimer.singleShot(200, show_success_message)
    
    def switch_to_program(self, program_name):
        """Switch to specified program"""
        print(f"Attempting to switch to program: {program_name}")
        
        # Add a brief delay to ensure enough time between hotkey operation and window activation
        import time
        time.sleep(0.1)
        
        success, error_message = self.window_manager.switch_to_program(program_name)
        
        if not success and error_message:
            print(f"Switching to program '{program_name}' failed: {error_message}")
            # Show beautified error message
            msg = QMessageBox(self)
            msg.setWindowTitle("Error")
            msg.setText(f"Cannot launch program '{program_name}'")
            msg.setInformativeText(error_message)
            msg.setIcon(QMessageBox.Critical)
            msg.setStyleSheet(ThemeManager.get_error_message_box_style(self.settings_manager.is_dark_mode))
            msg.exec_()
        else:
            print(f"Successfully switched to program: {program_name}")
    
    def closeEvent(self, event):
        """Handle window close event"""
        # Stop hotkey listening
        if self.settings_manager.hotkeys_enabled:
            self.hotkey_manager.stop_listening()
        
        # If floating window is enabled and visible, close it when the main window is closed
        if self.float_window and self.float_window.isVisible():
            self.float_window.close()
        
        event.accept()
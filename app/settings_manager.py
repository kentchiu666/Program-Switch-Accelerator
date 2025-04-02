# app/settings_manager.py
# Responsible for saving and loading settings, simplified hotkey functionality

import os
import json

class SettingsManager:
    """Settings management class, responsible for saving and loading program settings"""
    
    def __init__(self, version="Basic", max_programs=3):
        """Initialize settings manager"""
        # Set version
        self.version = version
        self.max_programs = max_programs
        
        # Settings path
        self.config_dir = os.path.join(os.path.expanduser("~"), ".program_switch_accelerator")
        self.config_file = os.path.join(self.config_dir, "config.json")
        
        # Ensure settings directory exists
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
        
        # Initialize program list and settings
        self.programs = ["", "", ""]
        self.float_window_enabled = False
        self.is_dark_mode = False
        self.hotkeys_enabled = False  # Simplified hotkey setting, only toggle without individual settings
        
        # Load settings
        self.load_settings()
    
    def load_settings(self):
        """Load settings"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                # Load program list
                if "programs" in config and isinstance(config["programs"], list):
                    # Only load up to the maximum allowed number of programs
                    for i in range(min(len(config["programs"]), self.max_programs)):
                        self.programs[i] = config["programs"][i]
                
                # Load floating window setting
                if "float_window_enabled" in config:
                    self.float_window_enabled = config["float_window_enabled"]
                
                # Load theme setting
                if "is_dark_mode" in config:
                    self.is_dark_mode = config["is_dark_mode"]
                
                # Load hotkey enable setting
                if "hotkeys_enabled" in config:
                    self.hotkeys_enabled = config["hotkeys_enabled"]
                
            except Exception as e:
                print(f"Error loading settings file: {e}")
    
    def save_settings(self, programs, float_window_enabled, is_dark_mode=None, hotkeys_enabled=None):
        """Save settings"""
        # Update settings
        self.programs = programs
        self.float_window_enabled = float_window_enabled
        
        # If dark mode setting is provided, update it
        if is_dark_mode is not None:
            self.is_dark_mode = is_dark_mode
        
        # If hotkey enable setting is provided, update it
        if hotkeys_enabled is not None:
            self.hotkeys_enabled = hotkeys_enabled
        
        # Save to configuration file
        config = {
            "version": self.version,
            "programs": self.programs,
            "float_window_enabled": self.float_window_enabled,
            "is_dark_mode": self.is_dark_mode,
            "hotkeys_enabled": self.hotkeys_enabled
        }
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=4)
        
        return True
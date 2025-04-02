# app/hotkey_manager.py - Fully Replaced Version

from PyQt5.QtCore import QObject, pyqtSignal
from pynput import keyboard
import threading
import time

class HotkeyManager(QObject):
    """Hotkey Manager class, responsible for listening and triggering hotkeys"""
    
    # Signal: sent when a hotkey is triggered
    hotkey_triggered = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.hotkeys = {}  # program name: hotkey
        self.listener = None
        self.running = False
        self.thread = None
    
    def start_listening(self):
        """Start listening for hotkeys"""
        print("Starting hotkey listening")
        
        # If already listening, return
        if self.running and self.thread and self.thread.is_alive():
            print("Hotkey listening is already running")
            return
        
        # Set flag and start new thread
        self.running = True
        self.thread = threading.Thread(target=self._listen_for_hotkeys)
        self.thread.daemon = True
        self.thread.start()
    
    def stop_listening(self):
        """Stop listening for hotkeys"""
        print("Stopping hotkey listening")
        
        # Set flag to exit the listening loop
        self.running = False
        
        # Stop the listener
        if self.listener:
            try:
                self.listener.stop()
            except Exception as e:
                print(f"Error stopping listener: {e}")
            self.listener = None
        
        # Wait for thread to end
        if self.thread:
            try:
                self.thread.join(timeout=0.5)
            except Exception as e:
                print(f"Error waiting for thread to end: {e}")
            self.thread = None
    
    def set_hotkeys(self, hotkeys):
        """Set hotkey mappings"""
        print(f"Setting hotkeys: {hotkeys}")
        hotkeys_changed = self.hotkeys != hotkeys
        self.hotkeys = hotkeys
        
        # If hotkeys have changed and currently listening, restart the listener
        if hotkeys_changed and self.running:
            print("Hotkeys have changed, restarting listener")
            self.stop_listening()
            time.sleep(0.2)  # Wait to ensure complete stop
            self.start_listening()
    
    def _listen_for_hotkeys(self):
        """Internal method for listening to hotkeys"""
        def on_press(key):
            if not self.running:
                return False
                
            try:
                # Check if it's a function key F1-F3
                if hasattr(key, 'name') and key.name in ['f1', 'f2', 'f3']:
                    key_name = key.name.upper()
                    print(f"Detected key: {key_name}")
                    
                    for program, hotkey in self.hotkeys.items():
                        if hotkey == key_name:
                            print(f"Triggering hotkey {key_name} for program: {program}")
                            # Send signal to notify main thread
                            self.hotkey_triggered.emit(program)
                            break
            except Exception as e:
                print(f"Hotkey processing error: {e}")
            
            return True
        
        try:
            # Create listener using pynput.keyboard.Listener
            self.listener = keyboard.Listener(on_press=on_press)
            self.listener.start()
            print("Keyboard listener started")
            
            # Keep thread running until stop flag is set to False
            while self.running:
                time.sleep(0.1)
                if not self.listener.is_alive():
                    print("Keyboard listener has stopped, attempting to restart")
                    self.listener = keyboard.Listener(on_press=on_press)
                    self.listener.start()
            
            print("Hotkey listening thread exited")
        except Exception as e:
            print(f"Keyboard listener error: {e}")
# app/window_manager.py
# Responsible for finding, activating and launching program windows

import os
import platform
import win32gui
import win32con
import pygetwindow as gw
import subprocess
import shutil
import json
import time
import sys

from app.program_mappings import ProgramMappings

class WindowManager:
    """Window Management class, responsible for finding, activating and launching program windows"""
    
    def __init__(self):
        # Special mappings for common programs
        self.special_programs = ProgramMappings.get_platform_mappings(platform.system())
        
        # Extended search paths
        self.common_program_paths = [
            os.environ.get('ProgramFiles', 'C:\\Program Files'),
            os.environ.get('ProgramFiles(x86)', 'C:\\Program Files (x86)'),
            os.path.join(os.environ.get('LocalAppData', ''), 'Programs'),
            os.environ.get('AppData', ''),
            os.path.join(os.environ.get('UserProfile', ''), 'AppData\\Local\\Microsoft\\WindowsApps'),
            os.path.join(os.environ.get('UserProfile', ''), 'AppData\\Local'),
            os.path.join(os.environ.get('UserProfile', ''), 'AppData\\Roaming'),
            os.path.join(os.environ.get('UserProfile', ''), 'Desktop')
        ]
        
        # Record of successfully launched program paths
        self.successful_paths = self._load_successful_paths()
    
    def _load_successful_paths(self):
        """Load record of successfully launched program paths"""
        config_dir = os.path.join(os.path.expanduser("~"), ".program_switch_accelerator")
        path_file = os.path.join(config_dir, "program_paths.json")
        
        if os.path.exists(path_file):
            try:
                with open(path_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading program path records: {e}")
                return {}
        return {}
    
    def _save_successful_path(self, program_name, program_path):
        """Save successfully launched program path"""
        config_dir = os.path.join(os.path.expanduser("~"), ".program_switch_accelerator")
        path_file = os.path.join(config_dir, "program_paths.json")
        
        # Ensure directory exists
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        
        # Load existing data
        paths = self._load_successful_paths()
        
        # Update data
        paths[program_name.lower()] = program_path
        
        # Save data
        try:
            with open(path_file, 'w', encoding='utf-8') as f:
                json.dump(paths, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"Error saving program path record: {e}")
            return False
    
    def switch_to_program(self, program_name):
        """Switch to specified program"""
        if not program_name:
            return False, None
        
        print(f"Attempting to switch to program: {program_name}")
        
        # Check if it's a special program
        lower_name = program_name.lower()
        exe_name = self.special_programs.get(lower_name, program_name)
        
        # Try to find open windows (using more flexible methods)
        found_windows = []
        
        # Method 1: Use full program name
        windows = gw.getWindowsWithTitle(program_name)
        if windows:
            found_windows.extend(windows)
            print(f"Found windows (using full name): {len(windows)}")
        
        # Method 2: Use partial program name
        if not found_windows:
            for window in gw.getAllWindows():
                if program_name.lower() in window.title.lower():
                    found_windows.append(window)
            if found_windows:
                print(f"Found windows (using partial name): {len(found_windows)}")
        
        # Method 3: If not found, use file name
        if not found_windows and "." in exe_name:
            program_base = exe_name.split(".")[0]
            windows = gw.getWindowsWithTitle(program_base)
            if windows:
                found_windows.extend(windows)
                print(f"Found windows (using file name): {len(windows)}")
        
        # If a matching window is found, activate it
        if found_windows:
            return self.activate_window(found_windows[0])
        
        # If no window is found, try to launch the program
        print(f"No window found, trying to launch program: {program_name}")
        try:
            success, message = self.start_program(program_name)
            return success, message
        except Exception as e:
            error_msg = str(e)
            print(f"Error launching program: {error_msg}")
            return False, error_msg
    
    def activate_window(self, window):
        """Enhanced window activation function, preserves original window state and ensures correct display"""
        try:
            print(f"Attempting to activate window: {window.title}")
            
            # Get window handle
            hwnd = window._hWnd
            
            # Check if window still exists
            if not win32gui.IsWindow(hwnd):
                return False, "Window no longer exists"
            
            # Get current display state of the window
            import win32api
            window_placement = win32gui.GetWindowPlacement(hwnd)
            show_cmd = window_placement[1]  # Get current display state
            was_maximized = (show_cmd == win32con.SW_SHOWMAXIMIZED)
            
            # 1. Check if window is off-screen, if so move it to visible area
            try:
                rect = win32gui.GetWindowRect(hwnd)
                x, y, right, bottom = rect
                width = right - x
                height = bottom - y
                
                # Check if off-screen
                screen_width = win32api.GetSystemMetrics(0)
                screen_height = win32api.GetSystemMetrics(1)
                
                if x < -width/2 or y < -height/2 or x > screen_width or y > screen_height:
                    print("Window is off-screen, moving to visible area")
                    new_x = max(0, min(x, screen_width - width))
                    new_y = max(0, min(y, screen_height - height))
                    win32gui.MoveWindow(hwnd, new_x, new_y, width, height, True)
            except Exception as e:
                print(f"Failed to move window: {e}")
            
            # 2. Check if window is minimized, if so restore it
            if win32gui.IsIconic(hwnd):
                print("Window is minimized, attempting to restore")
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                # Wait for window to restore
                time.sleep(0.2)
            
            # 3. Try multiple methods to activate window
            activation_success = False
            
            # Method 1: Use ShowWindow and SetForegroundWindow
            try:
                # Use original window state to display
                if was_maximized:
                    win32gui.ShowWindow(hwnd, win32con.SW_SHOWMAXIMIZED)
                else:
                    win32gui.ShowWindow(hwnd, win32con.SW_NORMAL)
                    
                win32gui.SetForegroundWindow(hwnd)
                activation_success = True
                print("Method 1 activation successful")
            except Exception as e:
                print(f"Method 1 activation failed: {e}")
            
            # Wait briefly
            time.sleep(0.2)
            
            # Check if window became foreground
            foreground_hwnd = win32gui.GetForegroundWindow()
            if foreground_hwnd != hwnd and not activation_success:
                # Method 2: Try alternative activation
                try:
                    # Simulate ALT+TAB (through key event simulation)
                    import win32com.client
                    shell = win32com.client.Dispatch("WScript.Shell")
                    shell.SendKeys("%{TAB}")  # ALT+TAB
                    time.sleep(0.1)
                    
                    # Then SetForegroundWindow again
                    win32gui.SetForegroundWindow(hwnd)
                    
                    # Restore maximized state
                    if was_maximized:
                        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
                    
                    activation_success = True
                    print("Method 2 activation successful")
                except Exception as e:
                    print(f"Method 2 activation failed: {e}")
            
            # Wait briefly
            time.sleep(0.1)
            
            # Check again, ensure window is visible and in foreground
            if foreground_hwnd != hwnd or not activation_success:
                # Method 3: Use WScript.Shell's AppActivate
                try:
                    shell = win32com.client.Dispatch("WScript.Shell")
                    shell.AppActivate(window.title)
                    
                    # Restore maximized state
                    if was_maximized:
                        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
                    
                    activation_success = True
                    print("Method 3 activation successful")
                except Exception as e:
                    print(f"Method 3 activation failed: {e}")
            
            # Method 4: Finally try using pygetwindow's method
            if not activation_success:
                try:
                    window.activate()
                    
                    # Restore window state
                    if was_maximized:
                        window.maximize()
                    
                    print("Method 4 activation successful")
                    activation_success = True
                except Exception as e:
                    print(f"Method 4 activation failed: {e}")
            
            # Final confirmation of window state
            if was_maximized:
                # Ensure window is still maximized
                try:
                    current_placement = win32gui.GetWindowPlacement(hwnd)
                    if current_placement[1] != win32con.SW_SHOWMAXIMIZED:
                        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
                        print("Reapplying maximized state")
                except Exception as e:
                    print(f"Failed to restore maximized state: {e}")
            
            return True, None
        except Exception as e:
            error_msg = f"Error activating window: {e}"
            print(error_msg)
            return False, error_msg
        
    def restore_window_if_minimized(self, window):
        """Restore window if minimized, returns True if window was restored"""
        try:
            # Use win32gui to check and restore window
            hwnd = window._hWnd  # Get window handle
            
            # Check if window is minimized
            if win32gui.IsIconic(hwnd):
                print("Window is minimized, attempting to restore")
                # Restore window
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                return True
            return False
        except Exception as e:
            print(f"Error restoring window: {e}")
            return False
    
    def start_program(self, program_name):
        """Start program"""
        print(f"Attempting to launch program: {program_name}")
        
        if platform.system() == "Windows":
            # Record attempted launch methods
            attempted_methods = []
            
            # 1. First check previously successful launch paths
            if program_name.lower() in self.successful_paths:
                path = self.successful_paths[program_name.lower()]
                attempted_methods.append(f"Using recorded successful path: {path}")
                try:
                    if path.lower().endswith('.lnk'):
                        # If it's a shortcut, get the target
                        target = self.get_exe_from_lnk(path)
                        if target:
                            subprocess.Popen(target)
                            print(f"Successfully launched program via shortcut: {target}")
                            return True, None
                    else:
                        subprocess.Popen(path)
                        print(f"Successfully launched program using recorded path: {path}")
                        return True, None
                except Exception as e:
                    print(f"Failed to launch using recorded path: {e}")
            
            # 2. Check if it's a special program
            lower_name = program_name.lower()
            if lower_name in self.special_programs:
                exe_name = self.special_programs[lower_name]
                attempted_methods.append(f"Using special program mapping: {exe_name}")
                
                # Special handling for Windows Settings
                if exe_name == "ms-settings:":
                    try:
                        os.startfile(exe_name)
                        print("Successfully launched Windows Settings")
                        return True, None
                    except Exception as e:
                        print(f"Failed to launch Windows Settings: {e}")
                
                # Special handling for Control Panel
                if exe_name == "control.exe":
                    try:
                        subprocess.Popen("control")
                        print("Successfully launched Control Panel")
                        return True, None
                    except Exception as e:
                        print(f"Failed to launch Control Panel: {e}")
                
                # Try direct launch of special program
                try:
                    os.startfile(exe_name)
                    print(f"Successfully launched special program: {exe_name}")
                    # Record successful path
                    self._save_successful_path(program_name, exe_name)
                    return True, None
                except Exception as e:
                    print(f"Failed to directly launch special program: {e}")
            
            # 3. Try to find program in Start Menu
            lnk_path = self.find_program_in_startmenu(program_name)
            if lnk_path:
                attempted_methods.append(f"Found in Start Menu: {lnk_path}")
                try:
                    # Get target from shortcut
                    target = self.get_exe_from_lnk(lnk_path)
                    if target:
                        subprocess.Popen(target)
                        print(f"Launched program via Start Menu shortcut: {target}")
                        # Record successful path
                        self._save_successful_path(program_name, target)
                        return True, None
                    else:
                        # Launch shortcut directly
                        os.startfile(lnk_path)
                        print(f"Directly launched Start Menu shortcut: {lnk_path}")
                        # Record successful path
                        self._save_successful_path(program_name, lnk_path)
                        return True, None
                except Exception as e:
                    print(f"Failed to launch via Start Menu: {e}")
            
            # 4. Try to launch with original program name
            attempted_methods.append(f"Attempting direct launch: {program_name}")
            try:
                os.startfile(program_name)
                print(f"Direct launch successful: {program_name}")
                # Record successful path
                self._save_successful_path(program_name, program_name)
                return True, None
            except Exception as e:
                print(f"Direct launch failed: {e}")
            
            # 5. Try adding .exe extension
            if not program_name.lower().endswith('.exe'):
                exe_name = f"{program_name}.exe"
                attempted_methods.append(f"Attempting with .exe extension: {exe_name}")
                try:
                    os.startfile(exe_name)
                    print(f"Launch with .exe extension successful: {exe_name}")
                    # Record successful path
                    self._save_successful_path(program_name, exe_name)
                    return True, None
                except Exception as e:
                    print(f"Launch with .exe extension failed: {e}")
            
            # 6. Try using cmd or bat file
            for ext in ['.bat', '.cmd']:
                file_name = f"{program_name}{ext}"
                attempted_methods.append(f"Attempting as batch file: {file_name}")
                try:
                    os.startfile(file_name)
                    print(f"Launch as batch file successful: {file_name}")
                    # Record successful path
                    self._save_successful_path(program_name, file_name)
                    return True, None
                except Exception as e:
                    print(f"Launch as batch file failed: {e}")
            
            # 7. Use 'where' command to find executable (only when command is available)
            if shutil.which("where"):
                attempted_methods.append("Using where command to search")
                try:
                    exe_path = subprocess.check_output(["where", program_name], universal_newlines=True).strip().split('\n')[0]
                    if exe_path:
                        subprocess.Popen(exe_path)
                        print(f"Found and launched using where command: {exe_path}")
                        # Record successful path
                        self._save_successful_path(program_name, exe_path)
                        return True, None
                except Exception as e:
                    print(f"Search using where command failed: {e}")
                
                # If program name needs .exe extension
                if not program_name.lower().endswith('.exe'):
                    attempted_methods.append(f"Using where command to search: {program_name}.exe")
                    try:
                        exe_path = subprocess.check_output(["where", f"{program_name}.exe"], universal_newlines=True).strip().split('\n')[0]
                        if exe_path:
                            subprocess.Popen(exe_path)
                            print(f"Found and launched using where command (adding .exe): {exe_path}")
                            # Record successful path
                            self._save_successful_path(program_name, exe_path)
                            return True, None
                    except Exception as e:
                        print(f"Search using where command (adding .exe) failed: {e}")
            
            # 8. Search common program installation locations
            exe_to_find = program_name
            if not exe_to_find.lower().endswith('.exe'):
                exe_to_find = f"{program_name}.exe"
            
            attempted_methods.append(f"Searching common installation locations: {exe_to_find}")
            for path in self.common_program_paths:
                if not path or not os.path.exists(path):
                    continue
                
                # Deep search for executable files (max two levels to avoid being too slow)
                for root, dirs, files in os.walk(path, topdown=True):
                    # Check filenames
                    possible_matches = []
                    for file in files:
                        # Exact match
                        if file.lower() == exe_to_find.lower():
                            possible_matches.append((file, 3))  # Priority 3: Exact match
                        # Partial match
                        elif program_name.lower() in file.lower() and file.lower().endswith('.exe'):
                            possible_matches.append((file, 2))  # Priority 2: Contains name and ends with .exe
                        # Fuzzy match
                        elif program_name.lower() in file.lower():
                            possible_matches.append((file, 1))  # Priority 1: Only contains name
                    
                    # Sort by priority
                    possible_matches.sort(key=lambda x: x[1], reverse=True)
                    
                    # Try to launch found programs
                    for match, _ in possible_matches:
                        full_path = os.path.join(root, match)
                        try:
                            subprocess.Popen(full_path)
                            print(f"Found and launched in {path}: {full_path}")
                            # Record successful path
                            self._save_successful_path(program_name, full_path)
                            return True, None
                        except Exception as e:
                            print(f"Failed to launch {full_path}: {e}")
                    
                    # Limit search depth
                    depth = root.count(os.path.sep) - path.count(os.path.sep)
                    if depth >= 2:  # If already searched two levels
                        dirs[:] = []  # Clear directory list, stop deeper search
            
            # 9. Try using Start Menu search
            attempted_methods.append("Attempting to launch using powershell")
            if shutil.which("powershell"):
                try:
                    ps_command = f'powershell.exe -Command "Start-Process \'{program_name}\'"'
                    subprocess.Popen(ps_command, shell=True)
                    print(f"Attempting to launch using PowerShell: {program_name}")
                    return True, None
                except Exception as e:
                    print(f"Launch using PowerShell failed: {e}")
            
            # All methods failed, give detailed suggestions
            failure_message = f"Unable to start program '{program_name}'. Attempted methods:\n"
            for i, method in enumerate(attempted_methods):
                failure_message += f"{i+1}. {method}\n"
            
            failure_message += "\nPlease try the following:\n"
            failure_message += "1. Ensure the program name is spelled correctly\n"
            failure_message += "2. Try entering the full program name (including file extension, such as .exe)\n"
            failure_message += "3. Find the program's executable and add it to the system environment variables\n"
            failure_message += "4. For common programs, try restarting the application and try again"
            
            return False, failure_message
        
        elif platform.system() == "Darwin":  # macOS
            import subprocess
            
            # macOS special program list
            lower_name = program_name.lower()
            app_name = self.special_programs.get(lower_name, program_name)
            
            try:
                subprocess.run(['open', '-a', app_name], check=True)
                return True, None
            except subprocess.CalledProcessError:
                # Try using mdfind to locate application
                try:
                    find_command = f'mdfind "kMDItemKind == Application && kMDItemDisplayName == \'{app_name}\'"'
                    app_path = subprocess.check_output(find_command, shell=True, universal_newlines=True).strip()
                    if app_path:
                        subprocess.run(['open', app_path], check=True)
                        return True, None
                except Exception:
                    pass
                    
                return False, f"Unable to start program '{program_name}'. Please ensure the program name is correct and installed, or try using the full application name."
        else:
            return False, f"Currently does not support {platform.system()} platform"
            
    def find_program_in_startmenu(self, program_name):
        """Find program in Start Menu"""
        start_menu_paths = [
            os.path.join(os.environ.get('ProgramData', 'C:\\ProgramData'), 'Microsoft\\Windows\\Start Menu\\Programs'),
            os.path.join(os.environ.get('AppData', ''), 'Microsoft\\Windows\\Start Menu\\Programs')
        ]
        
        for start_menu in start_menu_paths:
            if not os.path.exists(start_menu):
                continue
            
            # Search for .lnk files
            for root, dirs, files in os.walk(start_menu):
                for file in files:
                    if file.lower().endswith('.lnk') and program_name.lower() in file.lower():
                        return os.path.join(root, file)
        
        return None
    
    def get_exe_from_lnk(self, lnk_path):
        """Get executable file path from shortcut"""
        try:
            import win32com.client
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(lnk_path)
            return shortcut.Targetpath
        except Exception as e:
            print(f"Error getting target path from shortcut: {e}")
            return None
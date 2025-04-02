# app/program_mappings.py
class ProgramMappings:
    """Class to manage program name mappings"""
    
    @staticmethod
    def get_windows_mappings():
        """Get program mappings for Windows platform"""
        return {
            # Browsers
            "chrome": "chrome.exe",
            "google chrome": "chrome.exe",
            "firefox": "firefox.exe",
            "edge": "msedge.exe",
            "microsoft edge": "msedge.exe",
            "opera": "opera.exe",
            "brave": "brave.exe",
            "vivaldi": "vivaldi.exe",
            "internet explorer": "iexplore.exe",
            
            # Microsoft Office Suite
            "word": "winword.exe",
            "excel": "excel.exe",
            "powerpoint": "powerpnt.exe",
            "outlook": "OUTLOOK.EXE",
            "onenote": "ONENOTE.EXE",
            "access": "msaccess.exe",
            "publisher": "mspub.exe",
            "visio": "visio.exe",
            "project": "winproj.exe",
            
            # Adobe Suite
            "photoshop": "Photoshop.exe",
            "illustrator": "Illustrator.exe",
            "acrobat": "Acrobat.exe",
            "adobe reader": "AcroRd32.exe",
            "acrobat reader": "AcroRd32.exe",
            "after effects": "AfterFX.exe",
            "premiere": "Premiere Pro.exe",
            "premiere pro": "Premiere Pro.exe",
            "indesign": "InDesign.exe",
            "lightroom": "Lightroom.exe",
            
            # System Tools
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "cmd": "cmd.exe",
            "command prompt": "cmd.exe",
            "powershell": "powershell.exe",
            "explorer": "explorer.exe",
            "file explorer": "explorer.exe",
            "console": "control.exe",
            "control panel": "control.exe",
            "settings": "ms-settings:",
            "task manager": "taskmgr.exe",
            "disk cleanup": "cleanmgr.exe",
            "paint": "mspaint.exe",
            "registry editor": "regedit.exe",
            "wordpad": "wordpad.exe",
            "device manager": "devmgmt.msc",
            "system information": "msinfo32.exe",
            
            # Communication and Social Apps
            "teams": "Teams.exe",
            "microsoft teams": "Teams.exe",
            "slack": "slack.exe",
            "skype": "Skype.exe",
            "discord": "Discord.exe",
            "zoom": "Zoom.exe",
            "line": "LINE.exe",
            "wechat": "WeChat.exe",
            "telegram": "Telegram.exe",
            "whatsapp": "WhatsApp.exe",
            "qq": "QQ.exe",
            "webex": "webexapp.exe",
            
            # Development Tools
            "vscode": "Code.exe",
            "visual studio code": "Code.exe",
            "visual studio": "devenv.exe",
            "android studio": "studio64.exe",
            "intellij idea": "idea64.exe",
            "intellij": "idea64.exe",
            "pycharm": "pycharm64.exe",
            "webstorm": "webstorm64.exe",
            "eclipse": "eclipse.exe",
            "netbeans": "netbeans64.exe",
            "sublime text": "sublime_text.exe",
            "notepad++": "notepad++.exe",
            "git bash": "git-bash.exe",
            "github desktop": "GitHubDesktop.exe",
            
            # Multimedia Applications
            "spotify": "Spotify.exe",
            "vlc": "vlc.exe",
            "windows media player": "wmplayer.exe",
            "netflix": "Netflix.exe",
            "itunes": "iTunes.exe",
            "quicktime": "QuickTimePlayer.exe",
            "foobar2000": "foobar2000.exe",
            "winamp": "winamp.exe",
            "windows photos": "Microsoft.Photos.exe",
            "groove music": "Music.UI.exe",
            "films & tv": "Video.UI.exe",
            
            # Games and Gaming Platforms
            "steam": "steam.exe",
            "epic games": "EpicGamesLauncher.exe",
            "battle.net": "Battle.net.exe",
            "origin": "Origin.exe",
            "uplay": "upc.exe",
            "gog galaxy": "GalaxyClient.exe",
            "minecraft": "Minecraft.exe",
            "xbox": "XboxApp.exe",
            
            # Cloud Services and Storage
            "onedrive": "OneDrive.exe",
            "dropbox": "Dropbox.exe",
            "google drive": "googledrivesync.exe",
            "mega": "MEGAsync.exe",
            
            # Security Software
            "windows defender": "MSASCui.exe",
            "avast": "AvastUI.exe",
            "avg": "AVGUI.exe",
            "norton": "Norton.exe",
            "mcafee": "mcuimgr.exe",
            "kaspersky": "avpui.exe",
            "bitdefender": "bdagent.exe",
            
            # Virtualization
            "vmware": "vmware.exe",
            "virtualbox": "VirtualBox.exe",
            "hyper-v manager": "virtmgmt.msc",
            
            # Other Common Software
            "7-zip": "7zFM.exe",
            "winrar": "WinRAR.exe",
            "evernote": "Evernote.exe",
            "obs studio": "obs64.exe",
            "obs": "obs64.exe",
            "audacity": "audacity.exe",
            "blender": "blender.exe",
            "gimp": "gimp-2.10.exe",
            "calibre": "calibre.exe",
            "autocad": "acad.exe",
            "teamviewer": "TeamViewer.exe",
            "anydesk": "AnyDesk.exe",
            "filezilla": "filezilla.exe",
            "putty": "putty.exe",
            "ccleaner": "CCleaner64.exe"
        }
    
    @staticmethod
    def get_macos_mappings():
        """Get program mappings for macOS platform"""
        return {
            "chrome": "Google Chrome",
            "firefox": "Firefox",
            "safari": "Safari",
            "word": "Microsoft Word",
            "excel": "Microsoft Excel",
            "powerpoint": "Microsoft PowerPoint",
            "notes": "Notes",
            "terminal": "Terminal",
            "finder": "Finder",
            "system preferences": "System Preferences",
            "settings": "System Settings"
        }
    
    @staticmethod
    def get_platform_mappings(platform_name):
        """Get program mappings according to platform name"""
        if platform_name.lower() == "windows":
            return ProgramMappings.get_windows_mappings()
        elif platform_name.lower() == "darwin":  # macOS
            return ProgramMappings.get_macos_mappings()
        else:
            return {}  # Return empty dictionary for unsupported platforms
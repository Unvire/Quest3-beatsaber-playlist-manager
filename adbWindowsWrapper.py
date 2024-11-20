import os
import subprocess

class AdbFolderDoNotExist(Exception):
    pass

class AdbExeNotExist(Exception):
    pass

class AdbWindowsWrapper:
    def __init__(self):
        self.adbPath = os.path.join(os.getcwd(), 'adb')
        
        if not os.path.exists(self.adbPath):
            raise AdbFolderDoNotExist
        
        try:
            result = subprocess.run('adb/adb devices', capture_output=True, text=True)
            if 'List of devices attached' not in result.stdout:
                raise AdbExeNotExist
        except FileNotFoundError:
            raise AdbExeNotExist
        
    def getSongKeysFromQuest(self) -> list[str]:
        pass
    
    def getAndCopyPlaylistsFromQuest(self):
        pass

if __name__ == '__main__':
    a = AdbWindowsWrapper()

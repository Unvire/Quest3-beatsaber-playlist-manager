import os
import subprocess
import pyperclip

class AdbFolderDoNotExist(Exception):
    pass

class AdbExeNotExist(Exception):
    pass

class AdbWindowsWrapper:
    BEATSABER_SONGS_PATH = '/sdcard/ModData/com.beatgames.beatsaber/Mods/SongCore/CustomLevels'
    BEATSABER_PLAYLISTS_PATH = '/sdcard/ModData/com.beatgames.beatsaber/Mods/PlaylistManager/Playlists'

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
    
    def isDebugModeEnabled(self) -> bool:
        result = subprocess.run('adb/adb devices', capture_output=True, text=True).stdout
        lines = result.split('\n')
        return lines[1] != ''
        
    def getSongKeysFromQuest(self) -> list[str]:
        # coping to clipboard is a workaround about the fact that for some IDEs capturing stdo doesn't work
        command = f'adb shell ls {AdbWindowsWrapper.BEATSABER_SONGS_PATH} | clip'         
        result = self._executeAdbCommand(command)

        keys = [line.split(' ')[0] for line in result.split('\n')]
        return keys
    
    def getAndCopyPlaylistsFromQuest(self):
        # coping to clipboard is a workaround about the fact that for some IDEs capturing stdo doesn't work
        command = f'adb shell ls {AdbWindowsWrapper.BEATSABER_PLAYLISTS_PATH} | clip' 
        result = self._executeAdbCommand(command)
        playlists = [line for line in result.split('\n') if line]
        
        targetPath = os.path.join(os.getcwd(), 'tempPlaylists')
        if not os.path.exists(targetPath):
            os.makedirs(targetPath)
                
        for playlist in playlists:
            playlistPath = f'{AdbWindowsWrapper.BEATSABER_PLAYLISTS_PATH}/{playlist}'
            command = f'adb pull "{playlistPath}" "{targetPath}"'
            self._executeAdbCommand(command)
    
    def _executeAdbCommand(self, command:str) -> str:
        clipboard = pyperclip.paste()
        subprocess.run(command, shell=True, cwd=self.adbPath)
        result = pyperclip.paste()
        pyperclip.copy(clipboard)
        return result

if __name__ == '__main__':
    a = AdbWindowsWrapper()

    #user must allow debug access from computer
    isDebugModeEnabled = a.isDebugModeEnabled()
    print(f'Quest debug mode enabled: {isDebugModeEnabled}')

    #a.getSongKeysFromQuest()
    a.getAndCopyPlaylistsFromQuest()
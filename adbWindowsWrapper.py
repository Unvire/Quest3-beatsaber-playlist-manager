import os, subprocess
import pyperclip

class AdbWindowsWrapper:
    BEATSABER_SONGS_PATH = '/sdcard/ModData/com.beatgames.beatsaber/Mods/SongCore/CustomLevels'
    BEATSABER_PLAYLISTS_PATH = '/sdcard/ModData/com.beatgames.beatsaber/Mods/PlaylistManager/Playlists'

    def __init__(self):
        self.adbPath = os.path.join(os.getcwd(), 'adb')
    
    def checkIfInstalled(self) -> bool:        
        if not os.path.exists(self.adbPath):
            return False

        if not 'adb.exe' in os.listdir(self.adbPath):
            return False
        
        result = subprocess.run('adb/adb version', capture_output=True, text=True).stdout
        firstLine = result.splitlines()[0].lower()
        if 'android debug bridge' not in firstLine:
            return False
        return True

    def isDebugModeEnabled(self) -> bool:
        result = subprocess.run('adb/adb devices', capture_output=True, text=True).stdout
        firstDevice = result.splitlines()[1].lower()
        return firstDevice != '' and 'unauthorized' not in firstDevice
        
    def getSongKeysFromQuest(self) -> list[str]:
        # coping to clipboard is a workaround about the fact that for some IDEs capturing stdo doesn't work
        command = f'adb shell ls {AdbWindowsWrapper.BEATSABER_SONGS_PATH} | clip'         
        result = self._executeAdbCommand(command)

        keys = [line.split(' ')[0] for line in result.splitlines()]
        return keys
    
    def getPlaylistsNamesFromQuest(self) -> list[str]:
        # coping to clipboard is a workaround about the fact that for some IDEs capturing stdo doesn't work
        command = f'adb shell ls {AdbWindowsWrapper.BEATSABER_PLAYLISTS_PATH} | clip' 
        result = self._executeAdbCommand(command)
        playlists = [line for line in result.splitlines() if line]
        return playlists
    
    def pullPlaylistsFromQuest(self, playlistNamesList:list[str]):
        targetPath = os.path.join(os.getcwd(), 'playlists')
        if not os.path.exists(targetPath):
            os.makedirs(targetPath)
                
        for playlist in playlistNamesList:
            playlistPath = f'{AdbWindowsWrapper.BEATSABER_PLAYLISTS_PATH}/{playlist}'
            command = f'adb pull "{playlistPath}" "{targetPath}"'
            self._executeAdbCommand(command)
    
    def uploadPlaylistIntoQuest(self, filePath:str):
        command = f'adb push "{filePath}" "{AdbWindowsWrapper.BEATSABER_PLAYLISTS_PATH}"'
        self._executeAdbCommand(command)
    
    def deletePlaylistFromQuest(self, playlistName:str):
        command = f'adb shell rm "{AdbWindowsWrapper.BEATSABER_PLAYLISTS_PATH}/{playlistName}"'
        self._executeAdbCommand(command)
    
    def terminateAdb(self):
        subprocess.run('taskkill -f -im "adb.exe"', capture_output=True, text=True)
    
    def _executeAdbCommand(self, command:str) -> str:
        clipboard = pyperclip.paste()
        subprocess.run(command, shell=True, cwd=self.adbPath)
        result = pyperclip.paste()
        pyperclip.copy(clipboard)
        return result
    
    

if __name__ == '__main__':
    a = AdbWindowsWrapper()

    ## user must allow debug access from computer in the quest device
    isDebugModeEnabled = a.isDebugModeEnabled()
    print(f'Quest debug mode enabled: {isDebugModeEnabled}')

    keys = a.getSongKeysFromQuest()
    playlistNameList = a.getPlaylistsNamesFromQuest()
    a.pullPlaylistsFromQuest(playlistNameList)
    
    filepath = os.path.join(os.getcwd(), 'playlists', 'test.txt')
    #a.uploadPlaylistIntoQuest(filepath)
    #a.deletePlaylistFromQuest('test.txt')
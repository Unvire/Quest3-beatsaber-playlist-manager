import adbWindowsWrapper

class WrapperNotImplemented(Exception):
    pass

class AdbWrapperFactory():
    WRAPPERS = {
            'windows': adbWindowsWrapper.AdbWindowsWrapper
        }
    def __init__(self, osName:str):
        osName = osName.lower()
        
        try:
            self.adbWrapper = AdbWrapperFactory.WRAPPERS[osName]()
        except KeyError:
            raise WrapperNotImplemented
    
    def isDebugModeEnabled(self) -> bool:
        return self.adbWrapper.isDebugModeEnabled()
        
    def getSongKeysFromQuest(self) -> list[str]:
        return self.adbWrapper.getSongKeysFromQuest()
    
    def getPlaylistsNamesFromQuest(self) -> list[str]:
        self.adbWrapper.getPlaylistsNamesFromQuest()
    
    def pullPlaylistsFromQuest(self, playlistNamesList:list[str]):
        self.pullPlaylistsFromQuest(playlistNamesList)
    
    def uploadPlaylistIntoQuest(self, filePath:str):
        self.uploadPlaylistIntoQuest(filePath)
    
    def deletePlaylistFromQuest(self, playlistName:str):
        self.deletePlaylistFromQuest(playlistName)

if __name__ == '__main__':
    wrapper = AdbWrapperFactory('windows')
import requests, pyaudio, pydub
import io, threading

class ByteStringMusicPlayer():
    CHUNK_SIZE_BYTES = 1024

    def __init__(self):
        self.player = None
        self.stream = None  
        self.isPlaying = False 
        self.thread = None
        self.unconvertedByteString = ''
        self.fileFormat = ''

    def downloadMusicFromUrl(self, url:str) -> str:
        try:
            response = requests.get(url)
            unconvertedByteString = response.content
        except requests.exceptions.MissingSchema:
            unconvertedByteString = ''
        return unconvertedByteString
    
    def loadMusicFromByteStr(self, byteStr:str, fileFormat:str):
        self.unconvertedByteString = byteStr
        self.fileFormat = fileFormat
        self.thread = None
    
    def play(self):
        self.stop()
        if not isinstance(self.unconvertedByteString, bytes):
            return
        
        self.player = pyaudio.PyAudio()
        audio = pydub.AudioSegment.from_file(io.BytesIO(self.unconvertedByteString), 
                                             format=self.fileFormat)
        self.stream = self.player.open(format=self.player.get_format_from_width(audio.sample_width),
                                        channels=audio.channels,
                                        rate=audio.frame_rate,
                                        output=True)
        self.thread = threading.Thread(target=self._playAudioInChunks, args=(audio,))                
        self.isPlaying = True
        self.thread.start()
    
    def stop(self):
        self.isPlaying = False        
        if self.thread and self.thread.is_alive():
            self.thread.join()
            self.thread = None            
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        if self.player:
            self.player.terminate()
    
    def _playAudioInChunks(self, audio:pydub.AudioSegment):
        audioData = io.BytesIO(audio.raw_data)
        while self.isPlaying:
            chunk = audioData.read(ByteStringMusicPlayer.CHUNK_SIZE_BYTES)
            if not chunk:
                break
            self.stream.write(chunk)


if __name__ == '__main__':
    '''
    this class requires FFMPEG installed
    '''
    url = 'https://eu.cdn.beatsaver.com/b8c98ffc598703aadb4a3cb921d2830d270b57a5.mp3'
    fileFormat = 'mp3'
    
    a = ByteStringMusicPlayer()
    byteStr = a.downloadMusicFromUrl(url)
    a.loadMusicFromByteStr(byteStr, fileFormat)
    a.play()
    input('Press any key to stop...')
    a.stop()


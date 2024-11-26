import requests, pyaudio, pydub
import io, threading

class ByteStringMusicPlayer():
    CHUNK_SIZE_BYTES = 1024

    def __init__(self):
        self.player = pyaudio.PyAudio()
        self.stream = None                
        self.isPlaying = False 
        self.thread = None       

    def playFromUrl(self, url:str):
        response = requests.get(url)
        byteString = response.content

        fileFormat = url.split('.')[-1]
        audio = pydub.AudioSegment.from_file(io.BytesIO(byteString), format=fileFormat)
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
        self.player.terminate()
    
    def _playAudioInChunks(self, audio:pydub.AudioSegment):
        audio_data = io.BytesIO(audio.raw_data)
        while self.isPlaying:
            chunk = audio_data.read(ByteStringMusicPlayer.CHUNK_SIZE_BYTES)
            if not chunk:
                break
            self.stream.write(chunk)    
        self.isPlaying = False 


if __name__ == '__main__':
    '''
    this class requires FFMPEG installed
    '''
    a = ByteStringMusicPlayer()
    a.playFromUrl('https://eu.cdn.beatsaver.com/b8c98ffc598703aadb4a3cb921d2830d270b57a5.mp3')
    input('Press any key to stop...')
    a.stop()


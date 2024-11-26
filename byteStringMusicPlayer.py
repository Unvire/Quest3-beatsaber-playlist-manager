import requests
import pyaudio
from pydub import AudioSegment
import io

class ByteStringMusicPlayer():
    def __init__(self):
        self.player = pyaudio.PyAudio()
        self.stream = None

    def playFromUrl(self, url:str):
        response = requests.get(url)
        byteString = response.content

        fileFormat = url.split('.')[-1]
        audio = AudioSegment.from_file(io.BytesIO(byteString), format=fileFormat)
        self.stream = self.player.open(format=self.player.get_format_from_width(audio.sample_width),
                                        channels=audio.channels,
                                        rate=audio.frame_rate,
                                        output=True)
        
        self.stream(audio.raw_data)
    
    def stop(self):
        self.stream.stop_stream()
        self.stream.close()
        self.player.terminate()

if __name__ == '__main__':
    a = ByteStringMusicPlayer()
    a.playFromUrl('https://eu.cdn.beatsaver.com/b8c98ffc598703aadb4a3cb921d2830d270b57a5.mp3')

    input('Press any key to stop...')
    a.stop()


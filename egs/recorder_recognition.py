import sys
import pyaudio
p = pyaudio.PyAudio()
stream = p.open(format=p.get_format_from_width(2), channels=1, rate=44100, input=True)

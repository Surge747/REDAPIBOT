# test_tts.py

from tts_converter import text_to_speech

text = "This is a test of the text-to-speech function."
audio_path = "test_audio.mp3"
voice = 'en-US-AriaNeural'
rate = '+0%'

text_to_speech(text, audio_path, voice=voice, rate=rate)

import os

if os.path.exists(audio_path) and os.path.getsize(audio_path) > 0:
    print("TTS conversion successful. Audio file created.")
else:
    print("TTS conversion failed. No audio file created.")

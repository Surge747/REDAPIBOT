# tts_converter.py

import asyncio
import edge_tts
import os
import traceback

async def text_to_speech_async(text, filename, voice='en-US-AriaNeural', rate='+0%'):
    try:
        communicate = edge_tts.Communicate(text, voice=voice, rate=rate)
        await communicate.save(filename)
    except Exception as e:
        print(f"An error occurred during TTS conversion: {e}")
        traceback.print_exc()
        if os.path.exists(filename):
            os.remove(filename)  # Remove incomplete file
        raise  # Re-raise the exception to propagate it upwards

def text_to_speech(text, filename, voice='en-US-AriaNeural', rate='+0%'):
    asyncio.run(text_to_speech_async(text, filename, voice, rate))

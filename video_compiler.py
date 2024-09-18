# video_compiler.py

from moviepy.editor import (
    VideoFileClip,
    AudioFileClip,
    CompositeVideoClip,
    afx,
    ColorClip,
    CompositeAudioClip
)
import moviepy.config as moviepy_config
import os
import random

# Configure ImageMagick binary path (adjust the path as needed)
moviepy_config.change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16\magick.exe"})

def compile_video(audio_path, background_video_path, output_path, audio_duration, config):
    # Load audio
    final_audio = AudioFileClip(audio_path)

    # Load background video or create a black screen
    if background_video_path and os.path.exists(background_video_path):
        background_video = VideoFileClip(background_video_path)
        # Resize background video to desired resolution (e.g., 1080x1920)
        background_video = background_video.resize((1080, 1920))
        # Loop or cut the background video to match the audio duration
        if background_video.duration < audio_duration:
            background_video = background_video.loop(duration=audio_duration)
        else:
            background_video = background_video.subclip(0, audio_duration)
    else:
        # Create a black screen if no background video is provided
        background_video = ColorClip(size=(1080, 1920), color=(0, 0, 0), duration=audio_duration)

    # Composite the video
    video = CompositeVideoClip([background_video])
    video = video.set_audio(final_audio)

    # Add background music if provided
    if config.get('background_music_folder') and os.path.exists(config['background_music_folder']):
        music_files = [
            os.path.join(config['background_music_folder'], f)
            for f in os.listdir(config['background_music_folder'])
            if f.endswith(('.mp3', '.wav'))
        ]
        if music_files:
            background_music_file = random.choice(music_files)
            background_music = AudioFileClip(background_music_file).volumex(0.1)
            background_music = afx.audio_loop(background_music, duration=audio_duration)
            final_audio = CompositeAudioClip([background_music, final_audio])

    # Set final audio
    video = video.set_audio(final_audio)

    # Write the video file
    video.write_videofile(output_path, fps=24, codec='libx264')

    # Close clips to release resources
    video.close()
    final_audio.close()
    background_video.close()

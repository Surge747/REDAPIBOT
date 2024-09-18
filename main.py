# main.py

from reddit_extractor import fetch_reddit_posts, fetch_reddit_post_by_url
from tts_converter import text_to_speech
from video_compiler import compile_video
from youtube_uploader import upload_to_youtube
from moviepy.editor import AudioFileClip, concatenate_audioclips
import os
import random
import json

def split_text_into_chunks(text, max_chars=100):
    import re
    sentences = re.split(r'(?<=[.!?]) +', text)
    chunks = []
    current_chunk = ''
    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_chars:
            current_chunk += ' ' + sentence if current_chunk else sentence
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def main():
    # Load configuration from JSON file
    with open('config.json', 'r') as f:
        config = json.load(f)

    # Ensure directories exist
    os.makedirs('audio', exist_ok=True)

    # Configuration variables
    subreddits = config.get('subreddits', [])
    reddit_limit = config.get('reddit_limit', 5)
    background_videos_folder = config.get('background_videos_folder', 'background_videos/')
    background_music_folder = config.get('background_music_folder', 'background_music/')
    output_video_path = config.get('output_video_path', 'output_video.mp4')
    youtube_upload = config.get('youtube_upload', False)
    voice_name = config.get('default_voice', 'en-US-AriaNeural')
    rate = config.get('default_rate', '+0%')
    max_chars_per_chunk = config.get('max_chars_per_chunk', 100)
    comments_limit = config.get('comments_limit', 0)
    post_url = config.get('post_url', '')

    if post_url:
        # Fetch the specific post by URL
        print("Fetching Reddit post by URL...")
        post_data = fetch_reddit_post_by_url(post_url, comments_limit=comments_limit)
        if not post_data:
            print("Failed to fetch the post from the provided URL.")
            return
        subreddit_name = post_data['subreddit']
    else:
        # Subreddit selection
        print("Available subreddits:")
        for idx, subreddit in enumerate(subreddits):
            print(f"{idx+1}. {subreddit}")
        subreddit_selection = int(input("Select a subreddit by number: ")) - 1
        subreddit_name = subreddits[subreddit_selection]

        # Sort method selection
        sort_methods = ['hot', 'new', 'top', 'controversial', 'rising']
        print("Available sort methods:")
        for idx, method in enumerate(sort_methods):
            print(f"{idx+1}. {method}")
        sort_selection = int(input("Select a sort method by number: ")) - 1
        sort_method = sort_methods[sort_selection]

        # Fetch Reddit posts
        print("Fetching Reddit posts...")
        posts = fetch_reddit_posts(subreddit_name, sort=sort_method, limit=reddit_limit)
        if not posts:
            print("No suitable posts found.")
            return

        # Display posts for selection
        print("Available posts:")
        for idx, post in enumerate(posts):
            print(f"{idx+1}. {post['title'][:100]}")  # Display first 100 chars of title
        post_selection = int(input("Select a post by number: ")) - 1
        post_data = posts[post_selection]
        post_data['subreddit'] = subreddit_name

    # Prepare text content (post title + selftext)
    text_content = f"{post_data['title']}\n\n{post_data['selftext']}".strip()

    if not text_content:
        print("Error: The post has no content to process.")
        return

    # Split text into chunks for captions
    print("Splitting text into chunks for captions...")
    text_chunks = split_text_into_chunks(text_content, max_chars=max_chars_per_chunk)

    # Generate audio files and collect timings
    print("Generating audio and collecting timings...")
    audio_paths = []
    captions = []
    total_duration = 0.0

    for idx, chunk in enumerate(text_chunks):
        audio_path = os.path.join('audio', f"{post_data['id']}_part_{idx}.mp3")
        try:
            text_to_speech(chunk, audio_path, voice=voice_name, rate=rate)
        except Exception as e:
            print(f"An error occurred during TTS conversion: {e}")
            if os.path.exists(audio_path):
                os.remove(audio_path)
            return

        # Check if audio file was created and has content
        if not os.path.exists(audio_path) or os.path.getsize(audio_path) == 0:
            print(f"Error: Audio file {audio_path} was not created or is empty.")
            return  # Exit the script or handle the error as needed

        audio_clip = AudioFileClip(audio_path)
        duration = audio_clip.duration
        start_time = total_duration
        end_time = total_duration + duration
        total_duration += duration
        audio_paths.append(audio_path)
        captions.append({
            'text': chunk,
            'start_time': start_time,
            'end_time': end_time
        })
        audio_clip.close()

    # Select background video
    background_video = None
    if background_videos_folder and os.path.exists(background_videos_folder):
        videos = [
            os.path.join(background_videos_folder, f)
            for f in os.listdir(background_videos_folder)
            if f.endswith(('.mp4', '.mov'))
        ]
        if videos:
            background_video = random.choice(videos)

    # Compile video with captions
    print("Compiling video with captions...")
    compile_video(
        audio_paths,
        captions,
        background_video,
        output_video_path,
        config
    )

    print("Video compilation complete.")

    # Upload to YouTube (if enabled)
    if youtube_upload:
        print("Uploading to YouTube...")
        title = post_data['title']
        description = post_data['selftext']
        tags = ['Reddit', 'Story', subreddit_name]
        upload_to_youtube(output_video_path, title, description, tags)
        print("Upload complete.")

if __name__ == "__main__":
    main()

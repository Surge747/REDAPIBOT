# image_generator.py

from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

def generate_post_image(post_data, output_path, config):
    img_width = 1080
    background_color = (255, 255, 255)  # White background

    # Dynamically calculate image height based on content length
    content_text = post_data['selftext']
    content_lines = textwrap.wrap(content_text, width=40)
    total_lines = len(content_lines)
    img_height = 200 + (total_lines * 60)  # Adjust as needed

    # Create image
    img = Image.new('RGB', (img_width, img_height), color=background_color)
    draw = ImageDraw.Draw(img)

    # Load default font
    font_title = ImageFont.truetype("arial.ttf", size=60)
    font_username = ImageFont.load_default()
    font_content = ImageFont.load_default()

    # Set initial positions
    current_height = 20

    # Draw username and subreddit
    username_subreddit = f"u/{post_data['author']} • r/{post_data['subreddit']}"
    draw.text((50, current_height), username_subreddit, font=font_username, fill=(120, 124, 126))
    current_height += 30

    # Draw title
    title_lines = textwrap.wrap(post_data['title'], width=30)
    for line in title_lines:
        draw.text((50, current_height), line, font=font_title, fill=(0, 0, 0))
        current_height += 20

    current_height += 10  # Spacing

    # Draw selftext
    for line in content_lines:
        draw.text((50, current_height), line, font=font_content, fill=(0, 0, 0))
        current_height += 20

    # Save image
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path)

def generate_comment_images(comments, output_folder, config):
    images = []
    for idx, comment in enumerate(comments):
        img_width = 1080
        background_color = (255, 255, 255)  # White background

        # Dynamically calculate image height based on comment length
        comment_text = comment['body']
        content_lines = textwrap.wrap(comment_text, width=40)
        total_lines = len(content_lines)
        img_height = 100 + (total_lines * 20)  # Adjust as needed

        # Create image
        img = Image.new('RGB', (img_width, img_height), color=background_color)
        draw = ImageDraw.Draw(img)

        # Load default font
        font_username = ImageFont.load_default()
        font_content = ImageFont.load_default()

        # Set initial positions
        current_height = 20

        # Draw username
        draw.text((50, current_height), f"u/{comment['author']}", font=font_username, fill=(120, 124, 126))
        current_height += 30

        # Draw comment body
        for line in content_lines:
            draw.text((50, current_height), line, font=font_content, fill=(0, 0, 0))
            current_height += 20

        # Save image
        image_path = os.path.join(output_folder, f"comment_{idx}.png")
        img.save(image_path)
        images.append(image_path)

    return images

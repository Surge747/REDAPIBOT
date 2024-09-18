# image_cropper.py

from PIL import Image

def crop_screenshot(input_path, output_path, crop_area):
    """
    Crops the image at input_path to the area specified by crop_area
    and saves it to output_path.

    crop_area should be a tuple (left, upper, right, lower)
    """
    with Image.open(input_path) as img:
        cropped_img = img.crop(crop_area)
        cropped_img.save(output_path)

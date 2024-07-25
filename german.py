import cv2
import pytesseract
from PIL import Image
import os
import pyheif
import subprocess

def convert_heic_to_jpeg(heic_path, jpeg_path):
    try:
        # Use sips command to convert HEIC to JPEG
        subprocess.run(["sips", "-s", "format", "jpeg", heic_path, "--out", jpeg_path])
        return True
    except Exception as e:
        print(f"Error converting {heic_path} to JPEG: {e}")
        return False


def preprocess_image(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, thresh_image = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY)
    return thresh_image


def extract_text_from_image(image_path, lang='eng'):
    preprocessed_image = preprocess_image(image_path)
    if preprocessed_image is None:
        return None

    text = pytesseract.image_to_string(preprocessed_image, lang=lang)
    return text

convert_heic_to_jpeg("IMG_2602.HEIC","test_image3.jpg")

text = extract_text_from_image("test_image3.jpg", 'deu')

print(text)


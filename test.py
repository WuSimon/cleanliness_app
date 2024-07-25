import cv2
import pytesseract
import re

def preprocess_image(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    # Apply thresholding
    _, thresh_image = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY)
    return thresh_image

def extract_text_from_image(image_path):
    preprocessed_image = preprocess_image(image_path)
    text = pytesseract.image_to_string(preprocessed_image)
    return text

def parse_text(text):
    # Example regex patterns for parsing dates and amounts
    date_pattern = r'\d{2}/\d{2}/\d{4}'
    amount_pattern = r'\$\d+\.\d{2}'
    
    date_matches = re.findall(date_pattern, text)
    amount_matches = re.findall(amount_pattern, text)
    
    # Extracting the first match for simplicity
    date = date_matches[0] if date_matches else None
    amount = amount_matches[0] if amount_matches else None
    
    return {
        'date': date,
        'amount': amount,
        # Add more fields as necessary
    }


image_path = "test_image.png"

processed_image = preprocess_image(image_path)

cv2.imwrite("processed_image.png", processed_image)
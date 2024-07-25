import cv2
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import re
from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask import Flask, request, jsonify

app = Flask(__name__)

def preprocess_image(image_path):
    # Read the image in grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    # Apply thresholding
    _, thresh_image = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY)
    return thresh_image

def extract_text_from_image(image_path, lang='eng'):
    preprocessed_image = preprocess_image(image_path)
    # Perform OCR using the specified language
    text = pytesseract.image_to_string(preprocessed_image, lang=lang)
    return text

def parse_text(text):
    # Example regex patterns for parsing dates and amounts
    date_pattern = r'\d{2}/\d{2}/\d{4}'
    amount_pattern = r'\$\d+\.\d{2}'
    
    date_matches = re.findall(date_pattern, text)
    amount_matches = re.findall(amount_pattern, text)
    
    date = date_matches[0] if date_matches else None
    amount = amount_matches[0] if amount_matches else None
    
    return {
        'date': date,
        'amount': amount,
        # Add more fields as necessary
    }

def validate_data(data):
    if not data['date']:
        raise ValueError("Date not found")
    if not data['amount']:
        raise ValueError("Amount not found")
    return True

Base = declarative_base()

class Bill(Base):
    __tablename__ = 'bills'
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    amount = Column(Float)

engine = create_engine('sqlite:///bills.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def insert_data_into_db(data):
    bill = Bill(date=data['date'], amount=float(data['amount'].replace('$', '')))
    session.add(bill)
    session.commit()

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    lang = request.form.get('lang', 'eng')  # Default to English if no language is specified
    text = extract_text_from_image(file, lang)
    data = parse_text(text)
    validate_data(data)
    insert_data_into_db(data)
    return jsonify({"status": "success", "data": data})

if __name__ == '__main__':
    app.run(debug=True)

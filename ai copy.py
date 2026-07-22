import pytesseract
from PIL import Image

# Set the path to the Tesseract executable (adjust for your system)
pytesseract.pytesseract.tesseract_cmd = r'D:\Theory-Consepts\GenAI\Langchain\img' 

# Load the image
img = Image.open('sample_image.png')

# Perform OCR
text = pytesseract.image_to_string(img)
print(text)
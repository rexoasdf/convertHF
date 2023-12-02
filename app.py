from flask import Flask, request, jsonify
from PyPDF2 import PdfReader
from docx import Document
import pytesseract
from PIL import Image
import io

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert_document():
    if 'file' not in request.files:
        return "Nessun file fornito", 400

    file = request.files['file']
    file_extension = file.filename.split('.')[-1].lower()

    if file_extension == 'pdf':
        return convert_pdf_to_text(file)
    elif file_extension == 'docx':
        return convert_docx_to_text(file)
    elif file_extension in ['jpg', 'jpeg', 'png']:
        return perform_ocr(file)
    # Aggiungi qui ulteriori estensioni e metodi di conversione se necessario

    return "Formato file non supportato", 400

def convert_pdf_to_text(file_stream):
    reader = PdfReader(file_stream)
    text = " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
    return jsonify({'text': text})

def convert_docx_to_text(file_stream):
    doc = Document(file_stream)
    text = " ".join([para.text for para in doc.paragraphs])
    return jsonify({'text': text})

def perform_ocr(image_stream):
    image = Image.open(image_stream)
    text = pytesseract.image_to_string(image)
    return jsonify({'text': text})

if __name__ == '__main__':
    app.run(debug=True)

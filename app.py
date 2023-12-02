import streamlit as st
import os
import tempfile
import requests
from PyPDF2 import PdfReader
from docx import Document

# Funzione per processare i file PDF
def process_pdf(file_path):
    reader = PdfReader(file_path)
    text = " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
    return text

# Funzione per processare i file DOCX
def process_docx(file_path):
    doc = Document(file_path)
    text = " ".join([paragraph.text for paragraph in doc.paragraphs])
    return text

# Funzione per processare i file DOC (esempio per Windows)
def process_doc(file_path):
    import win32com.client as win32
    word = win32.Dispatch("Word.Application")
    word.visible = False
    doc = word.Documents.Open(file_path)
    text = doc.Range().Text
    doc.Close()
    word.Quit()
    return text

# Funzione per inviare il testo a un server tramite API
def send_text_to_api(text, api_url):
    try:
        response = requests.post(api_url, json={"text": text})
        if response.status_code == 200:
            return "Successo: Il testo è stato inviato all'API.", response.json()
        else:
            return f"Errore: Risposta API {response.status_code}", response.text
    except Exception as e:
        return f"Errore nell'invio dell'API: {e}", None

# Funzione principale dell'applicazione Streamlit
def main():
    st.title("Convertitore di File e Invio API")
    st.write("Carica un documento PDF, DOCX o DOC per convertirlo in testo e inviarlo a un endpoint API.")

    uploaded_file = st.file_uploader("Carica un file", type=["pdf", "docx", "doc"])
    api_url = st.text_input("Inserisci l'URL dell'API", "http://example.com/api")

    if st.button("Processa e Invia"):
        if uploaded_file and api_url:
            # Processamento del file
            with tempfile.NamedTemporaryFile(delete=False, suffix="." + uploaded_file.name.split('.')[-1]) as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                file_path = tmp_file.name

            file_extension = uploaded_file.name.split('.')[-1].lower()
            if file_extension == 'pdf':
                text = process_pdf(file_path)
            elif file_extension == 'docx':
                text = process_docx(file_path)
            elif file_extension == 'doc':
                text = process_doc(file_path)
            else:
                st.error("Formato file non supportato.")
                return

            os.remove(file_path)

            # Invio del testo all'API
            api_response, api_data = send_text_to_api(text, api_url)
            st.write(api_response)
            if api_data:
                st.json(api_data)
        else:
            st.error("Per favore carica un file e inserisci l'URL dell'API.")

if __name__ == "__main__":
    main()

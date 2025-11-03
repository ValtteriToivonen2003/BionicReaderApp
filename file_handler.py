import fitz  # pymupdf for pdf
from bs4 import BeautifulSoup  # beautifulsoup for html files

# autodetect file type
def extract_text(file_path):
    if file_path.lower().endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif file_path.lower().endswith('.html'):
        return extract_text_from_html(file_path)
    else:
        raise ValueError("Unsupported file type. Please use PDF or HTML files.")
# pdf importer
def extract_text_from_pdf(file_path):
    text = ""
    try:
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()
        return text
    except Exception as e:
        raise ValueError(f"Error reading PDF file: {str(e)}")

# import html files
def extract_text_from_html(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
        return soup.get_text()
    except Exception as e:
        raise ValueError(f"Error reading HTML file: {str(e)}")




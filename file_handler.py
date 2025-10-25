import fitz # is pymupdf for pdf
from bs4 import BeautifulSoup # is beautifulsoup for html files
from transcriber import transcribe_video # for video transcriber part

#autodetect file type
def extract_text(file_path):

    if file_path.endswith('.pdf'):
        return extract_text_from_pdf(file_path)

    elif file_path.endswith('.html'):
        return extract_text_from_html(file_path)

    elif file_path.endswith(('.mp4', '.mov', '.avi')):
        return extract_text_from_video

    else: 
        raise ValueError("unsupported file type")


# pdf importer 
def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    import fitz  # pymupdf for pdf
    from bs4 import BeautifulSoup  # beautifulsoup for html files


    # autodetect file type
    def extract_text(file_path):
        if file_path.endswith('.pdf'):
            return extract_text_from_pdf(file_path)
        elif file_path.endswith('.html'):
            return extract_text_from_html(file_path)
        else:
            raise ValueError("unsupported file type")


    # pdf importer
    def extract_text_from_pdf(file_path):
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text


    # import html files
    def extract_text_from_html(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
        return soup.get_text()




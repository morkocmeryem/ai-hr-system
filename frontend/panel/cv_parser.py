import pdfplumber
import unicodedata

def clean_text(text):
    return unicodedata.normalize("NFKC", text)

def fix_turkish_chars(text):
    replacements = {
        'ý': 'ı', 'þ': 'ş', 'ð': 'ğ', 'Ý': 'İ', 'Þ': 'Ş', 'Ð': 'Ğ'
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text

def extract_text_from_pdf(file_path):
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                page_text = clean_text(page_text)
                page_text = fix_turkish_chars(page_text)
                text += page_text
    except Exception as e:
        print("PDF okuma hatası:", e)
    return text

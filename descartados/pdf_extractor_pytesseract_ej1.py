import os
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
from PIL import Image
import pytesseract

# Configurar pytesseract (asegúrate de instalar Tesseract y establecer su ruta si no está en PATH)
# En Windows, por ejemplo:
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_pdf(pdf_path, ocr_enabled=True, ocr_lang='eng'):
    """
    Extrae texto de un archivo PDF usando PyPDF2 y pytesseract si es necesario.
    
    :param pdf_path: Ruta al archivo PDF.
    :param ocr_enabled: Si True, usa OCR para páginas complejas (como imágenes).
    :param ocr_lang: Idioma para el OCR (por defecto: inglés).
    :return: Texto extraído del PDF.
    """
    text = ""
    try:
        # Intentar extraer texto seleccionable
        reader = PdfReader(pdf_path)
        for page_num, page in enumerate(reader.pages, start=1):
            try:
                page_text = page.extract_text()
                if page_text and page_text.strip():
                    text += page_text
                elif ocr_enabled:
                    print(f"Usando OCR para la página {page_num}...")
                    text += ocr_page(pdf_path, page_num, ocr_lang)
            except Exception as e:
                print(f"Error al procesar la página {page_num}: {e}")
                if ocr_enabled:
                    text += ocr_page(pdf_path, page_num, ocr_lang)
    except Exception as e:
        print(f"Error al leer el PDF: {e}")
    return text

def ocr_page(pdf_path, page_num, ocr_lang='eng'):
    """
    Aplica OCR a una página específica de un PDF.
    
    :param pdf_path: Ruta al archivo PDF.
    :param page_num: Número de la página (comenzando en 1).
    :param ocr_lang: Idioma para el OCR.
    :return: Texto extraído por OCR.
    """
    try:
        # Convertir la página en imagen
        images = convert_from_path(pdf_path, first_page=page_num, last_page=page_num)
        if images:
            ocr_text = pytesseract.image_to_string(images[0], lang=ocr_lang)
            return ocr_text
    except Exception as e:
        print(f"Error al aplicar OCR a la página {page_num}: {e}")
    return ""

# Ejemplo de uso:
pdf_file_path = "ruta_a_tu_archivo.pdf"
extracted_text = extract_text_from_pdf(pdf_file_path, ocr_enabled=True, ocr_lang='spa')  
    # 'spa' para español
print(extracted_text)

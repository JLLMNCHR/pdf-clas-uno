import os
from PyPDF2 import PdfReader
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
from pdf2image import convert_from_path
import pytesseract

logging.basicConfig(
    filename='pdf_processing.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Declaración de contadores globales
ok_files = 0
ko_files = 0
total_files = 0

def extract_text_from_pdf(input_path, output_path, processed_folder):
    """
    Extrae texto de un archivo PDF utilizando OCR si es necesario.
    Mueve el PDF procesado a la carpeta PROCESADOS o a la carpeta ERROR si falla.
    """
    global ok_files, ko_files, total_files

    total_files += 1
    nom_fich = os.path.basename(input_path)
    print(f" .{total_files}-{nom_fich}", end='', flush=True)
    
    error_folder = os.path.join(os.path.dirname(output_path), 'ERROR')    
    
    try:
        
        text = ""
        # Intentar extraer texto seleccionable
        reader = PdfReader(input_path)
        for page_num, page in enumerate(reader.pages, start=1):
            try:
                page_text = page.extract_text()
                if page_text and page_text.strip():
                    text += page_text
                else:
                    text += ocr_page(input_path, page_num, 'spa')
            except Exception as e:                                
                text += ocr_page(input_path, page_num, 'spa')
        
        # Si el texto está vacío, mover el PDF a la carpeta ERROR
        if not text.strip():
            print("!", end='', flush=True)
            ko_files += 1
            logging.error(f"{nom_fich} Sin contenido")
            if not os.path.exists(error_folder):
                os.makedirs(error_folder)
            os.rename(input_path, os.path.join(error_folder, nom_fich))
            return

        # Guarda el texto extraído solo si hay contenido
        with open(output_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(text)

        # Mueve el PDF procesado a la carpeta PROCESADOS
        print(":", end='', flush=True)
        ok_files += 1
        os.rename(input_path, os.path.join(processed_folder, nom_fich))

    except Exception as e:
        print("X", end='', flush=True)
        ko_files += 1
        logging.error(f"{nom_fich} Excepción (1): {e}")
        if not os.path.exists(error_folder):
            os.makedirs(error_folder)
        os.rename(input_path, os.path.join(error_folder, nom_fich))

def process_pdfs(input_folder, output_folder, max_workers=1):
    """Procesa todos los PDFs, mueve los procesados a PROCESADOS y los que fallan a ERROR."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    processed_folder = os.path.join(output_folder, 'PROCESADOS')
    if not os.path.exists(processed_folder):
        os.makedirs(processed_folder)

    pdf_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.pdf')]
    #total_files = len(pdf_files)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(
                extract_text_from_pdf,
                os.path.join(input_folder, pdf_file),
                os.path.join(output_folder, os.path.splitext(pdf_file)[0] + '.txt'),
                processed_folder  # Pasa la carpeta PROCESADOS a la función
            ): pdf_file for pdf_file in pdf_files
        }

        for future in as_completed(futures):
            pdf_file = futures[future]
            try:
                future.result()
                # total_files += 1
            except Exception as e:
                nom_fich = os.path.basename(pdf_file)
                logging.error(f"{nom_fich} Excepción (2): {e}")

    print("\n");
    print(f"Total de archivos: {total_files}")
    print(f"Procesados correctamente: {ok_files}")
    print(f"Problemáticos: {ko_files}")

def ocr_page(pdf_path, page_num, ocr_lang='spa'):
    """
    Aplica OCR a una página específica de un PDF.
    
    :param pdf_path: Ruta al archivo PDF.
    :param page_num: Número de la página (comenzando en 1).
    :param ocr_lang: Idioma para el OCR.
    :return: Texto extraído por OCR.
    """
    # print(f"Usando OCR para la página {page_num}...")
    try:
        # Convertir la página en imagen
        images = convert_from_path(pdf_path, first_page=page_num, last_page=page_num)
        if images:
            ocr_text = pytesseract.image_to_string(images[0], lang=ocr_lang)
            return ocr_text
    except Exception as e:
        print("x", end='', flush=True)
        nom_fich = os.path.basename(pdf_path)
        logging.error(f"{nom_fich} Excepción al aplicar OCR a la página {page_num}: {e}")
    return ""

if __name__ == "__main__":
    import sys
    import time

    if len(sys.argv) != 3:
        print("Uso: python pdf_extractor_pytesseract.py <carpeta_entrada> <carpeta_salida>")
        sys.exit(1)

    input_folder = sys.argv[1]
    output_folder = sys.argv[2]

    start_time = time.time()
    process_pdfs(input_folder, output_folder)
    end_time = time.time()

    execution_time = end_time - start_time
    print(f"Tiempo de ejecución: {execution_time:.2f} segundos")



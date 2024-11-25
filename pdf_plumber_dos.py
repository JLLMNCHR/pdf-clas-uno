import os
import pdfplumber
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

# Add at the beginning of the file
logging.basicConfig(
    filename='pdf_processing.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def extract_text_from_pdf(input_path, output_path):
    """
    Extrae texto de un archivo PDF utilizando PdfPlumber y lo guarda en un archivo .txt.
    Si el texto extraído está vacío, mueve el PDF a la carpeta ERROR.
    """
    print(".", end='', flush=True)
    
    error_folder = os.path.join(os.path.dirname(output_path), 'ERROR')
    
    try:
        text = ""
        with pdfplumber.open(input_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""  # Maneja páginas sin texto

        # Si el texto está vacío, mover el PDF a la carpeta ERROR
        if not text.strip():
            print("!", end='', flush=True)
            logging.error(f"PDF sin contenido: {input_path}")

            if not os.path.exists(error_folder):
                os.makedirs(error_folder)
            error_file = os.path.join(error_folder, os.path.basename(input_path))
            os.rename(input_path, error_file)
            return

        # Guarda el texto extraído solo si hay contenido
        with open(output_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(text)

        print(":", end='', flush=True)
    
    except Exception as e:
        print("X", end='', flush=True)
        logging.error(f"Error procesando {input_path}: {e}")

        if not os.path.exists(error_folder):
            os.makedirs(error_folder)
        error_file = os.path.join(error_folder, os.path.basename(input_path))
        os.rename(input_path, error_file)

def process_pdfs(input_folder, output_folder, max_workers=4):
    """
    Procesa todos los PDFs en una carpeta de entrada y los convierte a texto.
    Maneja errores de forma segura.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    pdf_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.pdf')]
    total_files = len(pdf_files)
    processed_files = 0

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(
                extract_text_from_pdf,
                os.path.join(input_folder, pdf_file),
                os.path.join(output_folder, os.path.splitext(pdf_file)[0] + '.txt')
            ): pdf_file for pdf_file in pdf_files
        }

        for future in as_completed(futures):
            pdf_file = futures[future]
            try:
                future.result()
                processed_files += 1
            except Exception as e:
                print(f"Error procesando {pdf_file}: {e}")
    
    print(f"\nArchivos procesados: {processed_files} de {total_files}")

if __name__ == "__main__":
    import sys
    import time

    if len(sys.argv) != 3:
        print("Uso: python pdf_plumber_dos.py <carpeta_entrada> <carpeta_salida>")
        sys.exit(1)

    input_folder = sys.argv[1]
    output_folder = sys.argv[2]

    start_time = time.time()
    process_pdfs(input_folder, output_folder)
    end_time = time.time()

    execution_time = end_time - start_time
    print(f"Tiempo de ejecución: {execution_time:.2f} segundos")



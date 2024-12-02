import os
from docling.document_converter import DocumentConverter
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

logging.basicConfig(
    filename='pdf_processing.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Declaración de contadores globales
ok_files = 0
ko_files = 0

def extract_text_from_pdf(input_path, output_path, processed_folder):
    """
    Extrae texto de un archivo PDF utilizando PyMuPDF.
    Mueve el PDF procesado a la carpeta PROCESADOS o a la carpeta ERROR si falla.
    """
    print(".", end='', flush=True)
    
    global ok_files, ko_files
    error_folder = os.path.join(os.path.dirname(output_path), 'ERROR')    
    
    try:
        converter = DocumentConverter()
        text_aux = converter.convert(input_path)
        text = text_aux.document.export_to_markdown()
        
        # Si el texto está vacío, mover el PDF a la carpeta ERROR
        if not text.strip():
            print("!", end='', flush=True)
            ko_files += 1
            logging.error(f"PDF sin contenido: {input_path}")
            if not os.path.exists(error_folder):
                os.makedirs(error_folder)
            os.rename(input_path, os.path.join(error_folder, os.path.basename(input_path)))
            return

        # Guarda el texto extraído solo si hay contenido
        with open(output_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(text)

        # Mueve el PDF procesado a la carpeta PROCESADOS
        print(":", end='', flush=True)
        ok_files += 1
        os.rename(input_path, os.path.join(processed_folder, os.path.basename(input_path)))

    except Exception as e:
        print("X", end='', flush=True)
        ko_files += 1
        logging.error(f"Error procesando {input_path}: {e}")
        if not os.path.exists(error_folder):
            os.makedirs(error_folder)
        os.rename(input_path, os.path.join(error_folder, os.path.basename(input_path)))

def process_pdfs(input_folder, output_folder, max_workers=1):
    """Procesa todos los PDFs, mueve los procesados a PROCESADOS y los que fallan a ERROR."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    processed_folder = os.path.join(output_folder, 'PROCESADOS')
    if not os.path.exists(processed_folder):
        os.makedirs(processed_folder)

    pdf_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.pdf')]
    #total_files = len(pdf_files)
    total_files = 0

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
                total_files += 1
            except Exception as e:
                print(f"Error procesando {pdf_file}: {e}")

    print("\n");
    print(f"Total de archivos: {total_files}")
    print(f"Procesados correctamente: {ok_files}")
    print(f"Problemáticos: {ko_files}")

if __name__ == "__main__":
    import sys
    import time

    if len(sys.argv) != 3:
        print("Uso: python pdf_extractor_docling_varios.py <carpeta_entrada> <carpeta_salida>")
        sys.exit(1)

    input_folder = sys.argv[1]
    output_folder = sys.argv[2]

    start_time = time.time()
    process_pdfs(input_folder, output_folder)
    end_time = time.time()

    execution_time = end_time - start_time
    print(f"Tiempo de ejecución: {execution_time:.2f} segundos")



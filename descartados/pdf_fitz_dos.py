import os
import fitz  # PyMuPDF
from concurrent.futures import ThreadPoolExecutor, as_completed

def extract_text_from_pdf(input_path, output_path):
    """
    Extrae texto de un archivo PDF y lo guarda en un archivo .txt.
    Maneja errores específicos de archivos PDF malformados.
    """
    try:
        with fitz.open(input_path) as pdf:
            text = ""
            for page in pdf:
                text += page.get_text()
        
        # Guarda el texto extraído
        with open(output_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(text)

    except fitz.FileDataError as e:
        print(f"Archivo corrupto o no válido (PDF malformado): {input_path} - Error: {e}")
    except Exception as e:
        print(f"Error inesperado procesando {input_path}: {e}")

def process_pdfs(input_folder, output_folder, max_workers=4):
    """
    Procesa todos los PDFs en una carpeta de entrada y los convierte a texto.
    Maneja errores de forma segura.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    pdf_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.pdf')]

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
            except Exception as e:
                print(f"Error procesando {pdf_file}: {e}")

if __name__ == "__main__":
    import sys
    import time
        
    if len(sys.argv) != 3:
        print("Uso: python script.py <carpeta_entrada> <carpeta_salida>")
        sys.exit(1)

    input_folder = sys.argv[1]
    output_folder = sys.argv[2]

    start_time = time.time()
    process_pdfs(input_folder, output_folder)    
    end_time = time.time()
    
    execution_time = end_time - start_time
    print(f"Tiempo de ejecución: {execution_time:.2f} segundos")

    
